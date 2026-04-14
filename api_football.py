import requests
import os

API_KEY = os.environ.get("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


def get_team_data(team_name):

    try:
        # 🔍 TEAM ID
        res = requests.get(
            f"{BASE_URL}/teams?search={team_name}",
            headers=HEADERS,
            timeout=3
        )
        data = res.json()

        if not data.get("response"):
            return None

        team_id = data["response"][0]["team"]["id"]

        # 🔥 LAST MATCHES
        res = requests.get(
            f"{BASE_URL}/fixtures?team={team_id}&last=5",
            headers=HEADERS,
            timeout=3
        )
        matches = res.json().get("response", [])

        goals_for = []
        goals_against = []
        form_points = 0

        for m in matches:

            if m["teams"]["home"]["id"] == team_id:
                gf = m["goals"]["home"] or 0
                ga = m["goals"]["away"] or 0
            else:
                gf = m["goals"]["away"] or 0
                ga = m["goals"]["home"] or 0

            goals_for.append(gf)
            goals_against.append(ga)

            if gf > ga:
                form_points += 3
            elif gf == ga:
                form_points += 1

        # 🔥 blessures (simple)
        res = requests.get(
            f"{BASE_URL}/injuries?team={team_id}",
            headers=HEADERS,
            timeout=3
        )
        injuries = len(res.json().get("response", []))

        return {
            "attack": sum(goals_for) / len(goals_for) if goals_for else 1,
            "defense": sum(goals_against) / len(goals_against) if goals_against else 1,
            "form": form_points / 15,
            "injuries": injuries
        }

    except:
        return None