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
            "country": league["country"]["name"]
        })

    df = pd.DataFrame(leagues)
    df.to_csv("data_raw/leagues.csv", index=False)

    print("Leagues saved to data_raw/leagues.csv")