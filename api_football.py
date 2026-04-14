import requests
import os

API_KEY = os.environ.get("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


def get_today_matches():

    if not API_KEY:
        print("❌ API KEY manquante")
        return []

    matches = []

    try:
        res = requests.get(
            f"{BASE_URL}/fixtures?next=10",
            headers=HEADERS,
            timeout=3
        )

        data = res.json()

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

    except Exception as e:
        print("API ERROR:", e)
        return []


def get_odds(fixture_id):

    try:
        res = requests.get(
            f"{BASE_URL}/odds?fixture={fixture_id}",
            headers=HEADERS,
            timeout=3
        )

        data = res.json()

        if not data.get("response"):
            return None

        bookmakers = data["response"][0]["bookmakers"]

        for book in bookmakers:
            for bet in book["bets"]:

                if bet["name"] == "Match Winner":

                    values = bet["values"]

                    odds_dict = {v["value"]: float(v["odd"]) for v in values}

                    return (
                        odds_dict.get("Home"),
                        odds_dict.get("Draw"),
                        odds_dict.get("Away")
                    )

    except:
        return None

    return None