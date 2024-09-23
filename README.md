# LLM connections

Python code to evaluate a language model's abilityto solve [Connections](https://www.nytimes.com/games/connections) word puzzles.

This code was used to write [this post on my site](https://danielcorin.com/posts/2024/claude-3.5-sonnet-connections-evals/).

Note: there is a large amount of LLM-generated code in this project.

## High level approach

The idea behind this approach is to hold the model to a similar standard as a human player, within the restrictions of the game.
These standards include the following:

- The model is only prompted to make one guess at a time
- The model is given feedback after each guess including
  - if the guess was correct or incorrect
  - if 3/4 words were correct
  - if a guess was invalid (including a repeated group or if greater than or less than 4 words, or hallucinated words are proposed)
- If the model guesses 4 words that fit in a group, the guess is considered correct, even if the group description isn't correct

## Prompting

The model is given context about the game, a few example word groups, including a fully solved game with labelled categories, and prompted to former simple chain of thought inside `<scratchpad>` tags for _each guess_.

## Setup

Install dependencies

```sh
make venv
make install
```

### Other plugins

Other plugins can be found [here](https://llm.datasette.io/en/stable/plugins/directory.html).

### Add secrets
This project uses [`direnv`](https://direnv.net/#basic-installation).

```sh
cp .envrc.template .envrc
# add OPENAI_API_KEY
direnv allow
```

The remainder of the keys can be set/managed with

```sh
llm keys set <provider>
```

For example

```sh
llm keys set anthropic
```

I'm not exactly sure why this approach doesn't work for OpenAI models for me, but setting the environment variable seems to be a workaround.

## Run

```sh
python connections.py <model_name>
```

For example

```sh
python connections.py claude-3-opus
```


You can also specify a specific date for the game and use a custom prompt file:

```sh
python connections.py <model_name> --date YYYY-MM-DD --prompt path/to/custom_prompt.txt
```

For example:

```sh
python connections.py gpt-4o --date 2023-09-15 --prompt prompts/my_custom_prompt.txt
```

The --date option allows you to play a specific puzzle from the past, while the --prompt option lets you use a custom prompt file instead of the default one.

If no date is specified, the script will use today's date by default.
If no prompt file is specified, it will use the default prompt file.


