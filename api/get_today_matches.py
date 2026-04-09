import requests
import os
from datetime import datetime

API_KEY = os.getenv("3b63a56a290a3bd3d4b00c5b232d37d3")

headers = {
    "x-apisports-key": API_KEY
}

def get_today_matches():

    today = datetime.now().strftime("%Y-%m-%d")

    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "date": today
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    matches = []

    for m in data.get("response", []):

        match = {
            "league": m["league"]["name"],
            "home": m["teams"]["home"]["name"],
            "away": m["teams"]["away"]["name"],
            "time": m["fixture"]["date"][11:16]  # HH:MM
        }

        matches.append(match)

    return matches