from api_football import get_today_matches
from predict_match import predict_match


def get_top_bets():

    matches = get_today_matches()[:10]
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

        # 🔥 HOME fort
        if result["prob_home"] > 0.60:
            bets.append({
                "match": match,
                "bet": "HOME",
                "value": result["prob_home"],
                "odds": odd_home
            })

        # 🔥 AWAY fort
        elif result["prob_away"] > 0.60:
            bets.append({
                "match": match,
                "bet": "AWAY",
                "value": result["prob_away"],
                "odds": odd_away
            })

    return sorted(bets, key=lambda x: x["value"], reverse=True)[:8]