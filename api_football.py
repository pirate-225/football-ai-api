import requests
import os

API_KEY = os.environ.get("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


def get_team_last_matches(team_name):

    if not API_KEY:
        print("❌ API_KEY manquante")
        return None

    try:
        # 🔍 chercher team id
        res = requests.get(
            f"{BASE_URL}/teams?search={team_name}",
            headers=HEADERS,
            timeout=3
        )
        data = res.json()

        if not data.get("response"):
            return None

        team_id = data["response"][0]["team"]["id"]

        # 🔍 derniers matchs
        res = requests.get(
            f"{BASE_URL}/fixtures?team={team_id}&last=5",
            headers=HEADERS,
            timeout=3
        )
        data = res.json()

        matches = data.get("response", [])

        if not matches:
            return None

        goals_for = []
        goals_against = []

        for m in matches:

            if m["teams"]["home"]["id"] == team_id:
                goals_for.append(m["goals"]["home"] or 0)
                goals_against.append(m["goals"]["away"] or 0)
            else:
                goals_for.append(m["goals"]["away"] or 0)
                goals_against.append(m["goals"]["home"] or 0)

        return {
            "scored": sum(goals_for) / len(goals_for),
            "conceded": sum(goals_against) / len(goals_against)
        }

    except Exception as e:
        print("API ERROR:", e)
        return None