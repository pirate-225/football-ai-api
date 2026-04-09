import requests
import os

def get_today_matches():

    API_KEY = os.getenv("3b63a56a290a3bd3d4b00c5b232d37d3")

    if not API_KEY:
        return [{"league": "ERROR", "home": "API KEY", "away": "MISSING", "time": "--"}]

    url = "https://v3.football.api-sports.io/fixtures"

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "date": "2026-04-09"  # 🔥 FIXE pour test
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            return [{"league": "ERROR", "home": "STATUS", "away": str(response.status_code), "time": "--"}]

        data = response.json()

        matches = []

        for m in data.get("response", [])[:20]:

            matches.append({
                "league": m["league"]["name"],
                "home": m["teams"]["home"]["name"],
                "away": m["teams"]["away"]["name"],
                "time": m["fixture"]["date"][11:16]
            })

        if not matches:
            return [{"league": "INFO", "home": "NO MATCH", "away": "TODAY", "time": "--"}]

        return matches

    except Exception as e:
        return [{"league": "ERROR", "home": "EXCEPTION", "away": str(e), "time": "--"}]