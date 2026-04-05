import requests
import pandas as pd
from api.api_config import BASE_URL, HEADERS

def get_odds(league, season):
    url = BASE_URL + "odds"

    params = {
        "league": league,
        "season": season
    }

    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()

    odds_list = []

    for match in data["response"]:
        try:
            fixture_id = match["fixture"]["id"]

            bookmakers = match["bookmakers"]
            bets = bookmakers[0]["bets"]

            for bet in bets:
                if bet["name"] == "Match Winner":
                    values = bet["values"]
                    home_odds = values[0]["odd"]
                    draw_odds = values[1]["odd"]
                    away_odds = values[2]["odd"]

                    odds_list.append({
                        "fixture_id": fixture_id,
                        "home_odds": home_odds,
                        "draw_odds": draw_odds,
                        "away_odds": away_odds
                    })
        except:
            continue

    return pd.DataFrame(odds_list)