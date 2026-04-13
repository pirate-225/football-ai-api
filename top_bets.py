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

        edges = {
            "HOME": result["edge_home"],
            "DRAW": result["edge_draw"],
            "AWAY": result["edge_away"]
        }

        best_bet = max(edges, key=edges.get)
        best_edge = edges[best_bet]

        prob = result[f"prob_{best_bet.lower()}"]

        odds_map = {
            "HOME": odd_home,
            "DRAW": odd_draw,
            "AWAY": odd_away
        }

        odds = odds_map[best_bet]

        # 🔥 FILTRE ADAPTATIF (IMPORTANT)
        if best_edge > 0.015 and prob > 0.50:
            bets.append({
                "match": f"{m['home']} vs {m['away']}",
                "bet": best_bet,
                "edge": round(best_edge, 3),
                "value": round(prob, 3),
                "odds": odds
            })

    # 🔥 SI AUCUN BET → ON PREND LES MEILLEURS QUAND MÊME
    if len(bets) == 0:

        temp = []

        for m in today_matches:

            home = find_team(m["home"])
            away = find_team(m["away"])

            if home is None or away is None:
                continue

            odd_home, odd_draw, odd_away = m["odds"]

            result = predict_match(home, away, odd_home, odd_draw, odd_away)

            if result is None:
                continue

            edges = {
                "HOME": result["edge_home"],
                "DRAW": result["edge_draw"],
                "AWAY": result["edge_away"]
            }

            best_bet = max(edges, key=edges.get)

            temp.append({
                "match": f"{m['home']} vs {m['away']}",
                "bet": best_bet,
                "edge": round(edges[best_bet], 3),
                "value": round(result[f"prob_{best_bet.lower()}"], 3),
                "odds": m["odds"][0] if best_bet == "HOME" else m["odds"][2]
            })

        temp = sorted(temp, key=lambda x: x["edge"], reverse=True)

        return temp[:5]

    bets = sorted(bets, key=lambda x: x["edge"], reverse=True)

    return bets[:10]