import pandas as pd
from predict_match import predict_match
from api_football import get_today_matches

teams = pd.read_csv("data_processed/team_stats.csv")

# 🔥 NORMALISATION SIMPLE
def normalize(name):
    return name.lower().replace("fc", "").replace("cf", "").strip()


def find_team(api_name):
    api_name_n = normalize(api_name)

    for team in teams["Team"]:
        if normalize(team) in api_name_n or api_name_n in normalize(team):
            return team

    return None


def get_top_bets():

    matches = []
    today_matches = get_today_matches()

    print("📊 MATCHS API:", len(today_matches))

    for m in today_matches:

        home_api = m["home"]
        away_api = m["away"]

        home = find_team(home_api)
        away = find_team(away_api)

        if home is None or away is None:
            print(f"❌ Non trouvé: {home_api} vs {away_api}")
            continue

        odd_home, odd_draw, odd_away = m["odds"]

        result = predict_match(home, away, odd_home, odd_draw, odd_away)

        if result is None:
            continue

        prob_home = result["prob_home"]
        prob_away = result["prob_away"]

        edge_home = result["edge_home"]
        edge_away = result["edge_away"]

        confidence = result["confidence"]

        # 🔥 filtre assoupli pour test réel
        if (edge_home > 0.005 and prob_home > 0.45):
            matches.append({
                "match": f"{home_api} vs {away_api}",
                "bet": "HOME",
                "edge": edge_home,
                "confidence": confidence
            })

        elif (edge_away > 0.005 and prob_away > 0.45):
            matches.append({
                "match": f"{home_api} vs {away_api}",
                "bet": "AWAY",
                "edge": edge_away,
                "confidence": confidence
            })

    matches = sorted(matches, key=lambda x: x["edge"], reverse=True)

    print("✅ TOP BETS:", len(matches))

    return matches[:10]