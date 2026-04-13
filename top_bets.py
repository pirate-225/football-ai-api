import pandas as pd
from predict_match import predict_match
from api_football import get_today_matches

teams = pd.read_csv("data_processed/team_stats.csv")


def normalize(name):
    return (
        name.lower()
        .replace("fc", "")
        .replace("cf", "")
        .replace(".", "")
        .replace("-", "")
        .strip()
    )


def find_team(api_name):

    api_name_n = normalize(api_name)

    best_match = None
    best_score = 0

    for team in teams["Team"]:

        team_n = normalize(team)

        score = 0

        if team_n in api_name_n:
            score += 2
        if api_name_n in team_n:
            score += 2

        # 🔥 bonus mots communs
        for word in team_n.split():
            if word in api_name_n:
                score += 1

        if score > best_score:
            best_score = score
            best_match = team

    # 🔥 seuil minimum
    if best_score >= 2:
        return best_match

    return None


def get_top_bets():

    bets = []
    matches = get_today_matches()

    print("MATCHES:", len(matches))

    for m in matches:

        home = find_team(m["home"])
        away = find_team(m["away"])

        if home is None or away is None:
            print("SKIP:", m["home"], "vs", m["away"])
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

        bets.append({
            "match": f"{m['home']} vs {m['away']}",
            "bet": best_bet,
            "edge": edges[best_bet],
            "value": result[f"prob_{best_bet.lower()}"],
            "odds": odd_home if best_bet == "HOME" else odd_away
        })

    print("BETS FOUND:", len(bets))

    return sorted(bets, key=lambda x: x["edge"], reverse=True)[:10]