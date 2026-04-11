import requests
import os
from datetime import datetime

API_KEY = os.environ.get("3b63a56a290a3bd3d4b00c5b232d37d3")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"

def get_today_matches():

    if not API-KEY:
        print("❌ API_KEY manquante")
        return []

    today = datetime.today().strftime("%Y-%m-%d")

    url = f"{BASE_URL}/fixtures?date={today}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
    except:
        print("❌ API_KEY manquante")
        return []

    matches = []

    for m in data.get("response", []):

        fixture_id = m["fixture"]["id"]
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        odds = get_odds(fixture_id)

        if odds is None:
            continue

        matches.append({
            "home": home,
            "away": away,
            "odds": odds
        })

    return matches


def get_odds(fixture_id):

    url = f"{BASE_URL}/odds?fixture={fixture_id}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
    except:
        return None

    try:
        bookmakers = data["response"][0]["bookmakers"]

        for book in bookmakers:
            for bet in book["bets"]:
                if bet["name"] == "Match Winner":
                    values = bet["values"]

                    odd_home = float(values[0]["odd"])
                    odd_draw = float(values[1]["odd"])
                    odd_away = float(values[2]["odd"])

                    return (odd_home, odd_draw, odd_away)

    except:
        return None

    return None