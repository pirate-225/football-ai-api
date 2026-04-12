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

    matches = []
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

        if result["edge_home"] > 0.01:
            matches.append({
                "match": f"{m['home']} vs {m['away']}",
                "bet": "HOME",
                "edge": result["edge_home"]
            })

        elif result["edge_away"] > 0.01:
            matches.append({
                "match": f"{m['home']} vs {m['away']}",
                "bet": "AWAY",
                "edge": result["edge_away"]
            })

    return matches[:10]