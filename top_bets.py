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

        # 🔥 ON PREND TOUS LES EDGES (même petits)
        bets.append({
            "match": f"{m['home']} vs {m['away']}",
            "bet": "HOME",
            "edge": result["edge_home"],
            "value": result["prob_home"],
            "odds": odd_home
        })

        bets.append({
            "match": f"{m['home']} vs {m['away']}",
            "bet": "DRAW",
            "edge": result["edge_draw"],
            "value": result["prob_draw"],
            "odds": odd_draw
        })

        bets.append({
            "match": f"{m['home']} vs {m['away']}",
            "bet": "AWAY",
            "edge": result["edge_away"],
            "value": result["prob_away"],
            "odds": odd_away
        })

    # 🔥 TRIER PAR EDGE (IMPORTANT)
    bets = sorted(bets, key=lambda x: x["edge"], reverse=True)

    # 🔥 GARDER LES MEILLEURS (même si petits edges)
    best_bets = [b for b in bets if b["edge"] > -0.02][:15]

    return best_bets