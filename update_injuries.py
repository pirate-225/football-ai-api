import requests
import pandas as pd

API_KEY = "3b63a56a290a3bd3d4b00c5b232d37d3"

headers = {
    "x-apisports-key": API_KEY
}

league_ids = [39, 140, 135, 78, 61]  # élargissable

rows = []

for league in league_ids:
    url = f"https://v3.football.api-sports.io/injuries?league={league}&season=2025"

    res = requests.get(url, headers=headers).json()

    for item in res.get("response", []):
        team = item["team"]["name"]

        rows.append({
            "Team": team,
            "Injuries": 1
        })

df = pd.DataFrame(rows)

# compter blessures par équipe
df = df.groupby("Team").sum().reset_index()

df.to_csv("data_processed/injuries.csv", index=False)

print("✅ injuries updated")