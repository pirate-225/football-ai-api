import requests

API_KEY = "3b63a56a290a3bd3d4b00c5b232d37d3"

def get_live_data():

    url = "https://v3.football.api-sports.io/fixtures"

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "date": "2026-04-26"
    }

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5).json()

        matches = []

        for f in res["response"]:

            matches.append({
                "home": f["teams"]["home"]["name"],
                "away": f["teams"]["away"]["name"],
                "home_goals": f["goals"]["home"],
                "away_goals": f["goals"]["away"],
                "league": f["league"]["name"]
            })

        return matches

    except:
        return []