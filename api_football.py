import requests
import os

API_KEY = os.environ.get("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


def get_today_matches():

    if not API_KEY:
        return []

    try:
        res = requests.get(
            f"{BASE_URL}/fixtures?next=8",
            headers=HEADERS,
            timeout=3
        )

        data = res.json()

        matches = []

        for m in data.get("response", []):

            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]

            matches.append({
                "home": home,
                "away": away,
                "odds": (2.0, 3.2, 3.5)
            })

        return matches

    except:
        return []