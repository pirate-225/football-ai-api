import requests
import pandas as pd
import os

print("Downloading API data...")

API_KEY = "3b63a56a290a3bd3d4b00c5b232d37d3"

headers = {
    "x-apisports-key": API_KEY
}

url = "https://v3.football.api-sports.io/fixtures"

params = {
    "league": 39,   # Premier League
    "season": 2024
}

try:
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    fixtures = data.get("response", [])

    matches = []

    for f in fixtures:
        matches.append({
            "fixture_id": f["fixture"]["id"],
            "date": f["fixture"]["date"],
            "home_team": f["teams"]["home"]["name"],
            "away_team": f["teams"]["away"]["name"],
            "home_goals": f["goals"]["home"],
            "away_goals": f["goals"]["away"]
        })

    df = pd.DataFrame(matches)

    os.makedirs("data_raw", exist_ok=True)
    df.to_csv("data_raw/api_matches.csv", index=False)

    print("API data saved")

except Exception as e:
    print("API ERROR:", e)
    print("Continuing without API...")