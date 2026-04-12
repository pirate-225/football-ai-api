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

    for m in data.get("response", [])[:40]:

        fixture_date = datetime.fromisoformat(
            m["fixture"]["date"].replace("Z", "+00:00")
        )

        # 🔥 uniquement matchs FUTURS
        if fixture_date < now:
            continue

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        # 🔥 COTES SIMPLIFIÉES (rapide)
        odds = (1.80, 3.40, 4.20)

        matches.append({
            "home": home,
            "away": away,
            "odds": odds
        })

    return matches


# 🔥 NOUVEAU : FORME ÉQUIPE
def get_team_form(team_id):

    url = f"{BASE_URL}/fixtures?team={team_id}&last=5"

    try:
        res = requests.get(url, headers=HEADERS, timeout=5)
        data = res.json()
    except:
        return None

    goals = []
    conceded = []

    for m in data.get("response", []):

        home = m["teams"]["home"]["id"]
        away = m["teams"]["away"]["id"]

        if team_id == home:
            goals.append(m["goals"]["home"])
            conceded.append(m["goals"]["away"])
        else:
            goals.append(m["goals"]["away"])
            conceded.append(m["goals"]["home"])

    if not goals:
        return None

    return {
        "scored": sum(goals) / len(goals),
        "conceded": sum(conceded) / len(conceded)
    }