import pandas as pd

teams = pd.read_csv("data_processed/team_stats.csv")

def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    home_df = teams[teams["Team"] == home_team]
    away_df = teams[teams["Team"] == away_team]

    if home_df.empty or away_df.empty:
        return None  # 🔥 évite crash

    home = home_df.iloc[0]
    away = away_df.iloc[0]

    imp_home = 1 / float(odd_home)
    imp_draw = 1 / float(odd_draw)
    imp_away = 1 / float(odd_away)

    total_imp = imp_home + imp_draw + imp_away

    prob_home = imp_home / total_imp
    prob_draw = imp_draw / total_imp
    prob_away = imp_away / total_imp

    strength_home = (
        home["PPG"] * 0.5 +
        home["HomePPG"] * 0.3 +
        home["Form"] * 0.2
    )

    strength_away = (
        away["PPG"] * 0.5 +
        away["AwayPPG"] * 0.3 +
        away["Form"] * 0.2
    )

    diff = strength_home - strength_away
    adjustment = diff * 0.02

    prob_home += adjustment
    prob_away -= adjustment

    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    prob_over = min(0.75, (home["GoalsScoredAvg"] + away["GoalsScoredAvg"]) / 3)

    prob_btts = (
        (1 - home["FailToScoreRate"]) *
        (1 - away["FailToScoreRate"])
    )

    edge_home = prob_home - imp_home
    edge_draw = prob_draw - imp_draw
    edge_away = prob_away - imp_away

    confidence = max(prob_home, prob_draw, prob_away)

    return {
        "prob_home": round(float(prob_home), 3),
        "prob_draw": round(float(prob_draw), 3),
        "prob_away": round(float(prob_away), 3),
        "prob_over": round(float(prob_over), 3),
        "prob_btts": round(float(prob_btts), 3),
        "edge_home": round(float(edge_home), 3),
        "edge_draw": round(float(edge_draw), 3),
        "edge_away": round(float(edge_away), 3),
        "confidence": round(float(confidence), 3)
    }