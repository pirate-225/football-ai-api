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

        match_name = f"{m['home']} vs {m['away']}"

        # 🔥 on prend toujours le meilleur choix
        probs = {
            "HOME": result["prob_home"],
            "DRAW": result["prob_draw"],
            "AWAY": result["prob_away"]
        }

        best = max(probs, key=probs.get)

        odds_map = {
            "HOME": odd_home,
            "DRAW": odd_draw,
            "AWAY": odd_away
        }

        bets.append({
            "match": match_name,
            "bet": best,
            "value": probs[best],
            "edge": result[f"edge_{best.lower()}"],
            "odds": odds_map[best]
        })

    return sorted(bets, key=lambda x: x["value"], reverse=True)[:10]