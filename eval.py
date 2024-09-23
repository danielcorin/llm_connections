import asyncio
import hashlib
import json
import os
import argparse
from datetime import datetime, timedelta

from connections import (
    read_game_data,
    get_categories,
    LLMGuesser,
    Game,
    FIRST_GAME_DATE,
    START_MESSAGE,
)


def run_eval(prompt, model, game_date):
    # Fetch game data
    game_data = read_game_data(game_date)

    # Create categories
    categories = get_categories(game_data)

    # Initialize guesser and game
    guesser = LLMGuesser(model)
    game = Game(prompt, categories, guesser)

    won = game.play()
    print(won)

    game_state = game.result()
    return write_stats(prompt, model, game_date, game_state)


def write_stats(prompt, model, game_date, game_state):
    # Create a dictionary with the required information
    stats = {
        "model": model,
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest(),
        "game_date": game_date,
        "levels": {
            0: False,
            1: False,
            2: False,
            3: False,
        },
    }

    # Check which levels were correctly guessed
    for guess in game_state.correct_guesses():
        for category in game_state.categories:
            if guess.words == category.words:
                stats["levels"][category.level] = True
                break

    return stats


async def process_date(prompt, model, date_str, file_lock, filename):
    print(f"Checking evaluation for {date_str}")

    async with file_lock:
        with open(f"results/{filename}", "r") as f:
            for line in f:
                existing_stats = json.loads(line.strip())
                if (
                    existing_stats["model"] == model
                    and existing_stats["game_date"] == date_str
                ):
                    print(f"Evaluation for {date_str} already exists. Skipping.")
                    return existing_stats

    print(f"Running evaluation for {date_str}")
    stats = await asyncio.to_thread(run_eval, prompt, model, date_str)

    async with file_lock:
        with open(f"results/{filename}", "a") as f:
            json_stats = json.dumps(stats)
            f.write(json_stats + "\n")

    return stats


async def constrained_execution(funcs, max_runs):
    jobs = []
    semaphore = asyncio.Semaphore(max_runs)

    async def job(fn):
        async with semaphore:
            return await fn()

    for func in funcs:
        jobs.append(asyncio.ensure_future(job(func)))
    return await asyncio.gather(*jobs)


async def main():
    parser = argparse.ArgumentParser(
        description="Run evaluations for Connections game."
    )
    parser.add_argument("model", help="The model name to use for evaluation")
    parser.add_argument(
        "-p",
        "--parallelism",
        type=int,
        default=10,
        help="Number of parallel executions (default: 10)",
    )
    args = parser.parse_args()

    model = args.model
    prompt = START_MESSAGE

    os.makedirs("results", exist_ok=True)

    filename = f"{model}_{hashlib.sha256(prompt.encode()).hexdigest()}.jsonl"
    open(f"results/{filename}", "a").close()

    start_date = datetime.strptime(FIRST_GAME_DATE, "%Y-%m-%d").date()
    end_date = datetime.now().date()

    filename = f"{model}_{hashlib.sha256(prompt.encode()).hexdigest()}.jsonl"
    file_lock = asyncio.Lock()

    fns = []
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        fns.append(
            lambda d=date_str: process_date(prompt, model, d, file_lock, filename)
        )
        current_date += timedelta(days=1)

    all_stats = await constrained_execution(fns, args.parallelism)


if __name__ == "__main__":
    asyncio.run(main())
