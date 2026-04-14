from api_football import get_today_matches
from predict_match import predict_match


def get_top_bets():

    matches = get_today_matches()

    bets = []

    for m in matches:

        result = predict_match(
            m["home"],
            m["away"],
            m["odds"][0],
            m["odds"][1],
            m["odds"][2]
        )

        if result is None:
            continue

        match_name = f"{m['home']} vs {m['away']}"

        # 🔥 VALUE BET (1X2)
        if result["edge_home"] > 0.05 and result["prob_home"] > 0.55:
            bets.append({
                "match": match_name,
                "bet": "HOME",
                "value": result["prob_home"],
                "edge": result["edge_home"]
            })

        if result["edge_away"] > 0.05 and result["prob_away"] > 0.55:
            bets.append({
                "match": match_name,
                "bet": "AWAY",
                "value": result["prob_away"],
                "edge": result["edge_away"]
            })

        # 🔥 OVER 2.5
        if result["prob_over"] >= 0.65:
            bets.append({
                "match": match_name,
                "bet": "OVER 2.5",
                "value": result["prob_over"],
                "edge": None
            })

        # 🔥 BTTS
        if result["prob_btts"] >= 0.60:
            bets.append({
                "match": match_name,
                "bet": "BTTS YES",
                "value": result["prob_btts"],
                "edge": None
            })

    # 🔥 tri par probabilité
    bets = sorted(bets, key=lambda x: x["value"], reverse=True)

    return bets[:10]