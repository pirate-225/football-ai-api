import pandas as pd
import os
from api_football import get_team_last_matches

# 🔥 SAFE LOAD CSV
try:
    if os.path.exists("data_processed/team_stats.csv"):
        teams = pd.read_csv("data_processed/team_stats.csv")
    else:
        print("❌ CSV manquant")
        teams = pd.DataFrame()
except Exception as e:
    print("CSV ERROR:", e)
    teams = pd.DataFrame()


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    try:

        if teams.empty:
            return None

        home_df = teams[teams["Team"] == home_team]
        away_df = teams[teams["Team"] == away_team]

        if home_df.empty or away_df.empty:
            return None

        home = home_df.iloc[0]
        away = away_df.iloc[0]

        # 🔥 PAS D’API AU DÉMARRAGE (SAFE)
        home_attack = home["GoalsScoredAvg"]
        home_defense = home["GoalsConcededAvg"]

        away_attack = away["GoalsScoredAvg"]
        away_defense = away["GoalsConcededAvg"]

        home_strength = (home["PPG"] * 0.6 + home_attack * 0.3 - home_defense * 0.1) + 0.3
        away_strength = (away["PPG"] * 0.6 + away_attack * 0.3 - away_defense * 0.1)

        total = home_strength + away_strength

        prob_home = home_strength / total
        prob_away = away_strength / total
        prob_draw = max(0.1, 1 - (prob_home + prob_away))

        imp_home = 1 / float(odd_home)
        imp_draw = 1 / float(odd_draw)
        imp_away = 1 / float(odd_away)

        total_imp = imp_home + imp_draw + imp_away
        imp_home /= total_imp
        imp_draw /= total_imp
        imp_away /= total_imp

        return {
            "prob_home": round(prob_home, 3),
            "prob_draw": round(prob_draw, 3),
            "prob_away": round(prob_away, 3),
            "edge_home": round(prob_home - imp_home, 3),
            "edge_draw": round(prob_draw - imp_draw, 3),
            "edge_away": round(prob_away - imp_away, 3),
            "confidence": round(max(prob_home, prob_away), 3)
        }

    except Exception as e:
        print("MODEL ERROR:", e)
        return None