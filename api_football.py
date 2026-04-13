import requests
import os

API_KEY = os.environ.get("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


def get_team_last_matches(team_name):

    url = f"{BASE_URL}/teams?search={team_name}"

    try:
        res = requests.get(url, headers=HEADERS)
        team_data = res.json()
        team_id = team_data["response"][0]["team"]["id"]
    except:
        return None

    url = f"{BASE_URL}/fixtures?team={team_id}&last=5"

    try:
        res = requests.get(url, headers=HEADERS)
        matches = res.json()["response"]
    except:
        return None

    goals_for = []
    goals_against = []

    for m in matches:

        if m["teams"]["home"]["id"] == team_id:
            goals_for.append(m["goals"]["home"])
            goals_against.append(m["goals"]["away"])
        else:
            goals_for.append(m["goals"]["away"])
            goals_against.append(m["goals"]["home"])

    if not goals_for:
        return None

    return {
        "scored": sum(goals_for) / len(goals_for),
        "conceded": sum(goals_against) / len(goals_against)
    }