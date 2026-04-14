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

        edges = {
            "HOME": result["edge_home"],
            "DRAW": result["edge_draw"],
            "AWAY": result["edge_away"]
        }

        best = max(edges, key=edges.get)

        bets.append({
            "match": f"{m['home']} vs {m['away']}",
            "bet": best,
            "edge": edges[best]
        })

    return sorted(bets, key=lambda x: x["edge"], reverse=True)[:10]