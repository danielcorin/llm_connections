import httpx
import json
import os
from datetime import timedelta, datetime
from connections import FIRST_GAME_DATE


def main(url):
    if not os.path.exists("connections_data"):
        os.makedirs("connections_data")

    end_date = datetime.now()
    current_date = end_date

    while current_date >= datetime.strptime(FIRST_GAME_DATE, "%Y-%m-%d"):
        formatted_date = current_date.strftime("%Y-%m-%d")
        file_path = f"connections_data/{formatted_date}.json"

        if os.path.exists(file_path):
            print(f"Found existing file for {formatted_date}. Skipping.")
        else:
            print(f"Fetching data for {formatted_date}")
            u = url.format(date=formatted_date)
            response = httpx.get(u)
            response_object = response.json()

            with open(file_path, "w") as f:
                json.dump(response_object, f, indent=2)

        current_date -= timedelta(days=1)


if __name__ == "__main__":
    url = "https://www.nytimes.com/svc/connections/v2/{date}.json"
    main(url)
