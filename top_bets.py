import pandas as pd
from predict_match import predict_match
from api_football import get_today_matches

teams = pd.read_csv("data_processed/team_stats.csv")

def get_top_bets():

    matches = []
    today_matches = get_today_matches()

    for m in today_matches:

        home = m["home"]
        away = m["away"]
        odd_home, odd_draw, odd_away = m["odds"]

        if home not in teams["Team"].values or away not in teams["Team"].values:
            continue

        result = predict_match(home, away, odd_home, odd_draw, odd_away)

        if result is None:
            continue

        prob_home = result["prob_home"]
        prob_away = result["prob_away"]

        edge_home = result["edge_home"]
        edge_away = result["edge_away"]

        confidence = result["confidence"]

        if (edge_home > 0.02 and prob_home > 0.48 and confidence > 0.53):
            matches.append({
                "match": f"{home} vs {away}",
                "bet": "HOME",
                "edge": edge_home,
                "confidence": confidence
            })

        elif (edge_away > 0.02 and prob_away > 0.48 and confidence > 0.53):
            matches.append({
                "match": f"{home} vs {away}",
                "bet": "AWAY",
                "edge": edge_away,
                "confidence": confidence
            })

    matches = sorted(matches, key=lambda x: x["edge"], reverse=True)

    return matches[:10]