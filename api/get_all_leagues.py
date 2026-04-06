import requests
import pandas as pd
import os

API_KEY = "TA_CLE_API_ICI"

url = "https://v3.football.api-sports.io/leagues"

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(url, headers=headers)
data = response.json()

leagues = []

for item in data["response"]:
    league_id = item["league"]["id"]
    league_name = item["league"]["name"]
    country = item["country"]["name"]

    leagues.append([league_id, league_name, country])

df = pd.DataFrame(leagues, columns=["league_id", "league_name", "country"])

os.makedirs("data_raw", exist_ok=True)
df.to_csv("data_raw/leagues.csv", index=False)

print("All leagues saved")