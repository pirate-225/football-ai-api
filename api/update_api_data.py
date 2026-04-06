import requests
import pandas as pd
import os
import time

API_KEY = "3b63a56a290a3bd3d4b00c5b232d37d3"

headers = {
    "x-apisports-key": API_KEY
}

print("Loading leagues...")

leagues_df = pd.read_csv("data_raw/leagues.csv")

# Limite à 80 ligues pour éviter blocage
leagues_df = leagues_df.head(80)

big_leagues = [39, 140, 135, 78, 61]

all_matches = []

for _, row in leagues_df.iterrows():
    league_id = row["league_id"]
    league_name = row["league_name"]

    if league_id in big_leagues:
        seasons = [2022, 2023, 2024, 2025]
    else:
        seasons = [2024, 2025]

    for season in seasons:
        print("Downloading:", league_name, season)

        url = "https://v3.football.api-sports.io/fixtures"

        params = {
            "league": league_id,
            "season": season
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            fixtures = data.get("response", [])

            for f in fixtures:
                all_matches.append({
                    "fixture_id": f["fixture"]["id"],
                    "date": f["fixture"]["date"],
                    "HomeTeam": f["teams"]["home"]["name"],
                    "AwayTeam": f["teams"]["away"]["name"],
                    "FTHG": f["goals"]["home"],
                    "FTAG": f["goals"]["away"],
                    "league_id": league_id,
                    "league_name": league_name,
                    "season": season
                })

            time.sleep(1)

        except Exception as e:
            print("Error:", league_name, e)

df = pd.DataFrame(all_matches)

os.makedirs("data_raw", exist_ok=True)
df.to_csv("data_raw/api_matches_all_leagues.csv", index=False)

print("Download terminé")