import requests
import pandas as pd
from api.api_config import BASE_URL, HEADERS

def get_match_statistics(fixture_id):
    url = BASE_URL + "fixtures/statistics"

    params = {
        "fixture": fixture_id
    }

    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()

    stats = {}

    try:
        home_stats = data["response"][0]["statistics"]
        away_stats = data["response"][1]["statistics"]

        stats = {
            "fixture_id": fixture_id,
            "home_shots": home_stats[2]["value"],
            "away_shots": away_stats[2]["value"],
            "home_shots_on_target": home_stats[0]["value"],
            "away_shots_on_target": away_stats[0]["value"],
            "home_corners": home_stats[6]["value"],
            "away_corners": away_stats[6]["value"]
        }
    except:
        return None

    return stats