import requests
import os

API_KEY = os.environ.get("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


def get_match_odds(home_team, away_team):

    # 🔥 sécurité totale
    try:

        if not API_KEY:
            print("NO API KEY")
            return (2.0, 3.2, 3.5)

        res = requests.get(
            f"{BASE_URL}/fixtures?next=20",
            headers=HEADERS,
            timeout=3
        )

        data = res.json()

        for m in data.get("response", []):

            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]

            if home == home_team and away == away_team:

                fixture_id = m["fixture"]["id"]

                odds = get_odds_safe(fixture_id)

                if odds:
                    return odds

        # 🔥 fallback si match non trouvé
        return (2.0, 3.2, 3.5)

    except Exception as e:
        print("MATCH ODDS ERROR:", e)
        return (2.0, 3.2, 3.5)


def get_odds_safe(fixture_id):

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

            if book["name"] == "Bet365":

                for bet in book["bets"]:

                    if bet["name"] == "Match Winner":

                        values = bet["values"]

                        odds_dict = {
                            v["value"]: float(v["odd"])
                            for v in values
                        }

                        return (
                            odds_dict.get("Home"),
                            odds_dict.get("Draw"),
                            odds_dict.get("Away")
                        )

        return None

    except Exception as e:
        print("ODDS ERROR:", e)
        return None