import requests
import os
from datetime import datetime

def get_today_matches():

    API_KEY = os.getenv("3b63a56a290a3bd3d4b00c5b232d37d3")

    if not API_KEY:
        print("❌ API_KEY manquante")
        return []

    headers = {
        "x-apisports-key": API_KEY
    }

    today = datetime.now().strftime("%Y-%m-%d")

    print("📅 Date envoyée à API :", today)

    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "date": today
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        print("📡 Status API :", response.status_code)

        data = response.json()

        print("📊 Nombre de matchs reçus :", len(data.get("response", [])))

        matches = []

        for m in data.get("response", []):

            match = {
                "league": m["league"]["name"],
                "home": m["teams"]["home"]["name"],
                "away": m["teams"]["away"]["name"],
                "time": m["fixture"]["date"][11:16]
            }

            matches.append(match)

        return matches

    except Exception as e:
        print("❌ ERREUR API :", e)
        return []