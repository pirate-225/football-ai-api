import pandas as pd

teams = pd.read_csv("data_processed/team_stats.csv")


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    home = teams[teams["Team"] == home_team]
    away = teams[teams["Team"] == away_team]

    if home.empty or away.empty:
        return None

    home = home.iloc[0]
    away = away.iloc[0]

    # 🔥 modèle optimisé (sans API)
    home_strength = (
        home["PPG"] * 0.7 +
        home["GoalsScoredAvg"] * 0.2 -
        home["GoalsConcededAvg"] * 0.1
    ) + 0.35

    away_strength = (
        away["PPG"] * 0.7 +
        away["GoalsScoredAvg"] * 0.2 -
        away["GoalsConcededAvg"] * 0.1
    )

    total = home_strength + away_strength

    prob_home = home_strength / total
    prob_away = away_strength / total
    prob_draw = max(0.18, 1 - (prob_home + prob_away))

    # 🔥 bookmaker
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