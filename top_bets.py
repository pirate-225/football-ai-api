import pandas as pd
from predict_match import predict_match
from api_football import get_today_matches

teams = pd.read_csv("data_processed/team_stats.csv")


def normalize(name):
    return name.lower().replace("fc", "").replace(".", "").strip()


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

        # 🔥 PREND LE MEILLEUR EDGE (IMPORTANT)
        edges = {
            "HOME": result["edge_home"],
            "DRAW": result["edge_draw"],
            "AWAY": result["edge_away"]
        }

        best_bet = max(edges, key=edges.get)
        best_edge = edges[best_bet]

        # 🔥 FILTRE MINIMAL (TRÈS IMPORTANT)
        if best_edge < 0.01:
            continue

        odds_map = {
            "HOME": odd_home,
            "DRAW": odd_draw,
            "AWAY": odd_away
        }

        prob_map = {
            "HOME": result["prob_home"],
            "DRAW": result["prob_draw"],
            "AWAY": result["prob_away"]
        }

        bets.append({
            "match": f"{m['home']} vs {m['away']}",
            "bet": best_bet,
            "edge": round(best_edge, 3),
            "value": round(prob_map[best_bet], 3),
            "odds": odds_map[best_bet]
        })

    # 🔥 TRI PAR EDGE
    bets = sorted(bets, key=lambda x: x["edge"], reverse=True)

    return bets[:10]