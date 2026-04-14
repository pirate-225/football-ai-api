from api_football import get_today_matches
from predict_match import predict_match


def get_top_bets():

    matches = get_today_matches()

    bets = []

    for m in matches:

        odd_home, odd_draw, odd_away = m["odds"]

        result = predict_match(
            m["home"],
            m["away"],
            odd_home,
            odd_draw,
            odd_away
        )

        if result is None:
            continue

        match = f"{m['home']} vs {m['away']}"

        # 🔥 filtre PRO
        if result["prob_home"] > 0.60 and result["edge_home"] > 0.05:
            bets.append({
                "match": match,
                "bet": "HOME",
                "value": result["prob_home"],
                "edge": result["edge_home"],
                "odds": odd_home
            })

        if result["prob_away"] > 0.60 and result["edge_away"] > 0.05:
            bets.append({
                "match": match,
                "bet": "AWAY",
                "value": result["prob_away"],
                "edge": result["edge_away"],
                "odds": odd_away
            })

        if result["prob_over"] > 0.70:
            bets.append({
                "match": match,
                "bet": "OVER 2.5",
                "value": result["prob_over"],
                "edge": None,
                "odds": None
            })

        if result["prob_btts"] > 0.65:
            bets.append({
                "match": match,
                "bet": "BTTS YES",
                "value": result["prob_btts"],
                "edge": None,
                "odds": None
            })

    return sorted(bets, key=lambda x: x["value"], reverse=True)[:8]