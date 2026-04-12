import requests
import os
from datetime import datetime
import random

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
        print("❌ erreur API:", e)
        return []

    matches = []
    fixtures = data.get("response", [])

    print("📊 MATCHS TROUVÉS:", len(fixtures))

    for m in fixtures:

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        fixture_id = m["fixture"]["id"]

        odds = get_odds(fixture_id)

        # 🔥 SI PAS DE COTES → ON GENERE
        if odds is None:
            print(f"⚠️ Pas de cotes pour {home} vs {away} → fallback")

            # génération réaliste
            odd_home = round(random.uniform(1.4, 3.5), 2)
            odd_draw = round(random.uniform(2.8, 4.5), 2)
            odd_away = round(random.uniform(1.8, 4.5), 2)

            odds = (odd_home, odd_draw, odd_away)

        else:
            print(f"💰 {home} vs {away} → {odds}")

        matches.append({
            "home": home,
            "away": away,
            "odds": odds
        })

    print("✅ MATCHS UTILISÉS:", len(matches))

    return matches


def get_odds(fixture_id):

    url = f"{BASE_URL}/odds?fixture={fixture_id}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
    except:
        return None

    try:
        bookmakers = data["response"]

        if not bookmakers:
            return None

        bookmakers = bookmakers[0]["bookmakers"]

        for book in bookmakers:
            for bet in book["bets"]:
                if bet["name"] == "Match Winner":

                    values = bet["values"]

                    return (
                        float(values[0]["odd"]),
                        float(values[1]["odd"]),
                        float(values[2]["odd"])
                    )

    except:
        return None

    return None