import requests
import pandas as pd

API_KEY = "3b63a56a290a3bd3d4b00c5b232d37d3"

headers = {
    "x-apisports-key": API_KEY
}

url = "https://v3.football.api-sports.io/odds"

params = {
    "season": 2025
}

res = requests.get(url, headers=headers, params=params).json()

rows = []

for item in res.get("response", []):

    try:
        match = item["fixture"]["id"]
        odds = item["bookmakers"][0]["bets"][0]["values"]

        home = float(odds[0]["odd"])
        draw = float(odds[1]["odd"])
        away = float(odds[2]["odd"])

        rows.append({
            "fixture_id": match,
            "odd_home": home,
            "odd_draw": draw,
            "odd_away": away
        })

    except:
        continue

df = pd.DataFrame(rows)
df.to_csv("data_processed/odds.csv", index=False)

print("✅ odds updated")