import requests
import pandas as pd
from api.api_config import BASE_URL, HEADERS

def get_fixtures(league, season):
    url = BASE_URL + "fixtures"

    params = {
        "league": league,
        "season": season
    }

    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()

    matches = []

    for match in data["response"]:
        try:
            matches.append({
                "fixture_id": match["fixture"]["id"],
                "date": match["fixture"]["date"],
                "home_team": match["teams"]["home"]["name"],
                "away_team": match["teams"]["away"]["name"],
                "home_goals": match["goals"]["home"],
                "away_goals": match["goals"]["away"]
            })
        except:
            continue

    return pd.DataFrame(matches)