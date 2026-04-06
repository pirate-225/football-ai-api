import requests
import pandas as pd
import os

API_KEY = "3b63a56a290a3bd3d4b00c5b232d37d3"

headers = {
    "x-apisports-key": API_KEY
}

leagues = [
    39,   # Premier League
    140,  # La Liga
    135,  # Serie A
    78,   # Bundesliga
    61,   # Ligue 1
    88,   # Eredivisie
    94,   # Portugal
    71,   # Brazil
    128,  # Argentina
]

all_matches = []

for league in leagues:
    print("Downloading league:", league)

    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "league": league,
        "season": 2024
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    fixtures = data.get("response", [])

    for f in fixtures:
        match = {
            "fixture_id": f["fixture"]["id"],
            "date": f["fixture"]["date"],
            "home_team": f["teams"]["home"]["name"],
            "away_team": f["teams"]["away"]["name"],
            "home_goals": f["goals"]["home"],
            "away_goals": f["goals"]["away"]
        }
        all_matches.append(match)

df = pd.DataFrame(all_matches)

os.makedirs("data_raw", exist_ok=True)
df.to_csv("data_raw/api_matches.csv", index=False)

print("API matches saved")