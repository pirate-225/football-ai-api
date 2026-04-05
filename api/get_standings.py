import requests
import pandas as pd
from api.api_config import BASE_URL, HEADERS

def get_standings(league, season):
    url = BASE_URL + "standings"

    params = {
        "league": league,
        "season": season
    }

    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()

    standings_list = []

    try:
        standings = data["response"][0]["league"]["standings"][0]

        for team in standings:
            standings_list.append({
                "team": team["team"]["name"],
                "position": team["rank"],
                "points": team["points"],
                "goals_for": team["all"]["goals"]["for"],
                "goals_against": team["all"]["goals"]["against"]
            })
    except:
        return pd.DataFrame()

    return pd.DataFrame(standings_list)