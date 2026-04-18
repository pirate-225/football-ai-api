from api_football import get_today_matches
from predict_match import predict_match

def is_trap(result, odds):

    prob_home = result["prob_home"]
    prob_away = result["prob_away"]
    prob_draw = result["prob_draw"]

    edge_home = result["edge_home"]
    edge_away = result["edge_away"]

    odd_home, odd_draw, odd_away = odds

    # 🔥 1. match trop équilibré
    if abs(prob_home - prob_away) < 0.12:
        return True

    # 🔥 2. faux favori
    if prob_home > 0.65 and edge_home < 0.02:
        return True

    if prob_away > 0.65 and edge_away < 0.02:
        return True

    # 🔥 3. cotes trop basses
    if odd_home < 1.30 or odd_away < 1.30:
        return True

    # 🔥 4. draw dangereux
    if prob_draw > 0.28:
        return True

    # 🔥 5. edge suspect (trop élevé)
    if edge_home > 0.25 or edge_away > 0.25:
        return True

    return False


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

        if is_trap(result, (odd_home, odd_draw, odd_away)):
            continue

        match = f"{m['home']} vs {m['away']}"

        # 🔥 filtre intelligent
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