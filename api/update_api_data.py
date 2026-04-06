import requests
import pandas as pd
import os

API_KEY = "TA_CLE_API_ICI"

headers = {
    "x-apisports-key": API_KEY
}

leagues_df = pd.read_csv("data_raw/leagues.csv")

seasons = [2022, 2023, 2024]

all_matches = []

for _, row in leagues_df.iterrows():
    league_id = row["league_id"]

    for season in [2022, 2023, 2024, 2025]:
        print("Downloading league", league_id, "season", season)

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
                match = {
                    "fixture_id": f["fixture"]["id"],
                    "date": f["fixture"]["date"],
                    "HomeTeam": f["teams"]["home"]["name"],
                    "AwayTeam": f["teams"]["away"]["name"],
                    "FTHG": f["goals"]["home"],
                    "FTAG": f["goals"]["away"],
                    "league_id": league_id,
                    "season": season
                }

                all_matches.append(match)

        except:
            print("Error league", league_id)

df = pd.DataFrame(all_matches)

os.makedirs("data_raw", exist_ok=True)
df.to_csv("data_raw/api_matches_all_leagues.csv", index=False)

print("All matches downloaded")