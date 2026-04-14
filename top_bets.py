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

        probs = {
            "HOME": result["prob_home"],
            "DRAW": result["prob_draw"],
            "AWAY": result["prob_away"]
        }

        best = max(probs, key=probs.get)

        bets.append({
            "match": f"{m['home']} vs {m['away']}",
            "bet": best,
            "prob": probs[best]
        })

    return bets[:10]