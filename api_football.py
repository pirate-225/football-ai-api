import requests
import os

API_KEY = os.environ.get("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


def safe_request(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=3)
        return res.json()
    except:
        return None


def get_today_matches():

    if not API_KEY:
        return []

    data = safe_request(f"{BASE_URL}/fixtures?next=8")

    if not data or "response" not in data:
        return []

    matches = []

    for m in data["response"]:

        try:
            fixture_id = m["fixture"]["id"]
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]

            odds = get_odds_safe(fixture_id)

            if not odds:
                odds = (2.0, 3.2, 3.5)

            matches.append({
                "home": home,
                "away": away,
                "odds": odds
            })

        except:
            continue

    return matches


def get_odds_safe(fixture_id):

    data = safe_request(f"{BASE_URL}/odds?fixture={fixture_id}")

    if not data or "response" not in data or not data["response"]:
        return None

    try:
        bookmakers = data["response"][0]["bookmakers"]

        for book in bookmakers:

            if book.get("name") == "Bet365":

                for bet in book.get("bets", []):

                    if bet.get("name") == "Match Winner":

                        values = bet.get("values", [])

                        odds_dict = {
                            v["value"]: float(v["odd"])
                            for v in values
                        }

                        return (
                            odds_dict.get("Home"),
                            odds_dict.get("Draw"),
                            odds_dict.get("Away")
                        )

    except:
        return None

    return None