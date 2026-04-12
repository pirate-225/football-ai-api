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

        # 🔥 SCORE GLOBAL
        score = max(
            result["prob_home"],
            result["prob_away"],
            result["prob_over"],
            result["prob_btts"]
        )

        # 🔥 TYPE DE BET
        if result["prob_over"] == score:
            bet_type = "OVER 2.5"
        elif result["prob_btts"] == score:
            bet_type = "BTTS YES"
        elif result["prob_home"] == score:
            bet_type = "HOME"
        else:
            bet_type = "AWAY"

        bets.append({
            "match": f"{m['home']} vs {m['away']}",
            "bet": bet_type,
            "value": round(score, 3),
            "odds": odd_home if bet_type == "HOME" else odd_away
        })

    # 🔥 TRI PAR QUALITÉ
    bets = sorted(bets, key=lambda x: x["value"], reverse=True)

    return bets[:10]