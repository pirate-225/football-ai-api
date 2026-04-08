import pandas as pd
import joblib

teams = pd.read_csv("data_processed/team_stats.csv")

model_result = joblib.load("models/model_result.pkl")
model_over = joblib.load("models/model_over.pkl")
model_btts = joblib.load("models/model_btts.pkl")

def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    home = teams[teams["Team"] == home_team].iloc[0]
    away = teams[teams["Team"] == away_team].iloc[0]

    home_ppg = home["PointsPerGame"]
    away_ppg = away["PointsPerGame"]

    home_goal_diff = home["GoalDiff"]
    away_goal_diff = away["GoalDiff"]

    home_form = home["Form"]
    away_form = away["Form"]

    ppg_diff = home_ppg - away_ppg
    goal_diff_diff = home_goal_diff - away_goal_diff
    form_diff = home_form - away_form

    strength_home = home_ppg + home_goal_diff
    strength_away = away_ppg + away_goal_diff
    strength_diff = strength_home - strength_away

    X = [[
        home_ppg,
        away_ppg,
        ppg_diff,
        goal_diff_diff,
        form_diff,
        strength_diff
    ]]

    probs = model_result.predict_proba(X)[0]

    prob_home = probs[0]
    prob_draw = probs[1]
    prob_away = probs[2]

    prob_over = model_over.predict_proba(X)[0][1]
    prob_btts = model_btts.predict_proba(X)[0][1]

    # EDGE
    edge_home = prob_home - (1 / float(odd_home))
    edge_draw = prob_draw - (1 / float(odd_draw))
    edge_away = prob_away - (1 / float(odd_away))

    confidence = max(prob_home, prob_draw, prob_away)

    return {
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "prob_over": round(prob_over, 3),
        "prob_btts": round(prob_btts, 3),
        "edge_home": round(edge_home, 3),
        "edge_draw": round(edge_draw, 3),
        "edge_away": round(edge_away, 3),
        "confidence": round(confidence, 3)
    }