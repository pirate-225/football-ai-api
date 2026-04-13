import pandas as pd
from api_football import get_team_last_matches

teams = pd.read_csv("data_processed/team_stats.csv")


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    try:

        home_df = teams[teams["Team"] == home_team]
        away_df = teams[teams["Team"] == away_team]

        if home_df.empty or away_df.empty:
            return None

        home = home_df.iloc[0]
        away = away_df.iloc[0]

        # 🔥 API FORM (safe)
        home_form = get_team_last_matches(home_team)
        away_form = get_team_last_matches(away_team)

        home_attack = home_form["scored"] if home_form else home["GoalsScoredAvg"]
        home_defense = home_form["conceded"] if home_form else home["GoalsConcededAvg"]

        away_attack = away_form["scored"] if away_form else away["GoalsScoredAvg"]
        away_defense = away_form["conceded"] if away_form else away["GoalsConcededAvg"]

        # 🔥 force
        home_strength = (home["PPG"] * 0.5 + home_attack * 0.3 - home_defense * 0.2) + 0.3
        away_strength = (away["PPG"] * 0.5 + away_attack * 0.3 - away_defense * 0.2)

        total = home_strength + away_strength

        prob_home = home_strength / total
        prob_away = away_strength / total
        prob_draw = max(0.1, 1 - (prob_home + prob_away))

        # bookmaker
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