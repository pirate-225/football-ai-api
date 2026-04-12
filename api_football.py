import requests
import os
from datetime import datetime, timezone

API_KEY = os.environ.get("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


def get_today_matches():

    if not API_KEY:
        return []

    today = datetime.now().strftime("%Y-%m-%d")

    url = f"{BASE_URL}/fixtures?date={today}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        data = response.json()
    except:
        return []

    matches = []

    now = datetime.now(timezone.utc)

    for m in data.get("response", [])[:30]:

        fixture_date = datetime.fromisoformat(m["fixture"]["date"].replace("Z", "+00:00"))

        # 🔥 FILTRE MATCHS FUTURS UNIQUEMENT
        if fixture_date < now:
            continue

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        # ⚠️ simplifié pour performance
        odds = (1.80, 3.50, 4.00)

        matches.append({
            "home": home,
            "away": away,
            "odds": odds
        })

    return matches