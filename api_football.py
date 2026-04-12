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
        print("❌ API_KEY manquante")
        return []

    today = datetime.today().strftime("%Y-%m-%d")
    print("📅 DATE:", today)

    url = f"{BASE_URL}/fixtures?date={today}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
        print("✅ API fixtures OK")
    except Exception as e:
        print("❌ erreur API fixtures:", e)
        return []

    matches = []

    fixtures = data.get("response", [])
    print("📊 NB MATCHS API:", len(fixtures))

    for m in fixtures:

        fixture_id = m["fixture"]["id"]
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        print(f"➡️ {home} vs {away}")

        odds = get_odds(fixture_id)

        if odds is None:
            print("❌ Pas de cotes")
            continue

        print("💰 Odds:", odds)

        matches.append({
            "home": home,
            "away": away,
            "odds": odds
        })

    print("✅ MATCHS UTILISABLES:", len(matches))

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