import requests
import pandas as pd
from api.api_config import BASE_URL, HEADERS

def get_leagues():
    url = BASE_URL + "leagues"

    response = requests.get(url, headers=HEADERS)
    data = response.json()

    leagues = []

    for league in data["response"]:
        leagues.append({
            "league_id": league["league"]["id"],
            "league_name": league["league"]["name"],
            "country": league["country"]["name"],
            "type": league["league"]["type"]
        })

    df = pd.DataFrame(leagues)

    # garder seulement les ligues
    df = df[df["type"] == "League"]

    df.to_csv("data_raw/leagues.csv", index=False)

    print("Leagues saved to data_raw/leagues.csv")


if __name__ == "__main__":
    get_leagues()