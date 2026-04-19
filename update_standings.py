import requests
import pandas as pd

API_KEY = "3b63a56a290a3bd3d4b00c5b232d37d3"

headers = {
    "x-apisports-key": API_KEY
}

league_ids = [39, 140, 135, 78, 61]  # tu peux élargir

rows = []

for league in league_ids:
    url = f"https://v3.football.api-sports.io/standings?league={league}&season=2025"

    res = requests.get(url, headers=headers).json()

    try:
        standings = res["response"][0]["league"]["standings"][0]

        for team in standings:
            rows.append({
                "Team": team["team"]["name"],
                "Rank": team["rank"],
                "Points": team["points"]
            })

    except:
        continue

df = pd.DataFrame(rows)
df.to_csv("data_processed/standings.csv", index=False)

print("✅ standings updated")