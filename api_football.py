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
        print("✅ Fixtures récupérées")
    except Exception as e:
        print("❌ erreur fixtures:", e)
        return []

    matches = []

    for m in data.get("response", []):

        fixture_id = m["fixture"]["id"]
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        odds = get_odds(fixture_id)

        if odds is None:
            print(f"❌ Pas de cotes pour {home} vs {away}")
            continue

        print(f"💰 {home} vs {away} → {odds}")

        matches.append({
            "home": home,
            "away": away,
            "odds": odds
        })

    print("✅ MATCHS AVEC COTES:", len(matches))

    return matches


def get_odds(fixture_id):

    url = f"{BASE_URL}/odds?fixture={fixture_id}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
    except:
        return None

    try:
        if not data["response"]:
            return None

        bookmakers = data["response"][0]["bookmakers"]

        for bookmaker in bookmakers:
            for bet in bookmaker["bets"]:

                # 🔥 IMPORTANT : Match Winner = "Match Winner"
                if bet["name"] == "Match Winner":

                    values = bet["values"]

                    odds_dict = {v["value"]: float(v["odd"]) for v in values}

                    odd_home = odds_dict.get("Home")
                    odd_draw = odds_dict.get("Draw")
                    odd_away = odds_dict.get("Away")

                    if odd_home and odd_draw and odd_away:
                        return (odd_home, odd_draw, odd_away)

    except Exception as e:
        print("❌ erreur parsing odds:", e)
        return None

    return None