import requests
import os
from datetime import datetime, timezone

API_KEY = os.environ.get("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


def get_today_matches():

    today = datetime.now().strftime("%Y-%m-%d")

    url = f"{BASE_URL}/fixtures?date={today}"

    try:
        res = requests.get(url, headers=HEADERS, timeout=5)
        data = res.json()
    except:
        return []

    matches = []
    now = datetime.now(timezone.utc)

    for m in data.get("response", [])[:20]:

        fixture_id = m["fixture"]["id"]

        fixture_date = datetime.fromisoformat(
            m["fixture"]["date"].replace("Z", "+00:00")
        )

        # 🔥 matchs futurs uniquement
        if fixture_date < now:
            continue

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
        res = requests.get(url, headers=HEADERS, timeout=5)
        data = res.json()
    except:
        return None

    try:
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