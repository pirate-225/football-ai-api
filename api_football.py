import requests
import os
from datetime import datetime

API_KEY = os.environ.get("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


def get_today_matches():

    if not API_KEY:
        return []

    today = datetime.today().strftime("%Y-%m-%d")

    url = f"{BASE_URL}/fixtures?date={today}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        data = response.json()
    except:
        return []

    matches = []

    # 🔥 LIMITE À 20 MATCHS MAX
    fixtures = data.get("response", [])[:20]

    for m in fixtures:

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        # 🔥 PAS D’API ODDS (trop lent)
        # on utilise odds simplifiées

        matches.append({
            "home": home,
            "away": away,
            "odds": (1.80, 3.50, 4.00)
        })

    return matches