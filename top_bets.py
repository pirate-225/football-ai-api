import pandas as pd
from predict_match import predict_match
from api_football import get_today_matches

teams = pd.read_csv("data_processed/team_stats.csv")


def normalize(name):
    return name.lower().replace("fc", "").strip()


def find_team(api_name):
    api_name_n = normalize(api_name)

    for team in teams["Team"]:
        if normalize(team) in api_name_n or api_name_n in normalize(team):
            return team

    return None


def get_top_bets():

    bets = []
    today_matches = get_today_matches()

    for m in today_matches:

        home = find_team(m["home"])
        away = find_team(m["away"])

        if home is None or away is None:
            continue

        odd_home, odd_draw, odd_away = m["odds"]

        result = predict_match(home, away, odd_home, odd_draw, odd_away)

        if result is None:
            continue

        # 🔥 OVER BET
        if result["prob_over"] > 0.70:
            bets.append({
                "match": f"{m['home']} vs {m['away']}",
                "bet": "OVER 2.5",
                "value": result["prob_over"]
            })

        # 🔥 BTTS
        if result["prob_btts"] > 0.65:
            bets.append({
                "match": f"{m['home']} vs {m['away']}",
                "bet": "BTTS YES",
                "value": result["prob_btts"]
            })

        # 🔥 WINNER (seulement si fort)
        if result["prob_home"] > 0.60:
            bets.append({
                "match": f"{m['home']} vs {m['away']}",
                "bet": "HOME",
                "value": result["prob_home"]
            })

        elif result["prob_away"] > 0.60:
            bets.append({
                "match": f"{m['home']} vs {m['away']}",
                "bet": "AWAY",
                "value": result["prob_away"]
            })

    bets = sorted(bets, key=lambda x: x["value"], reverse=True)

    return bets[:15]