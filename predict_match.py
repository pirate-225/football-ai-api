import pandas as pd
import joblib

team_stats = pd.read_csv("data_processed/team_stats.csv")

model_result = joblib.load("models/model_result.pkl")
model_over = joblib.load("models/model_over.pkl")
model_btts = joblib.load("models/model_btts.pkl")

def predict_match(home_team, away_team, odds_home, odds_draw, odds_away):

    home_stats = team_stats[team_stats["Team"] == home_team].iloc[0]
    away_stats = team_stats[team_stats["Team"] == away_team].iloc[0]

    features = [[
        home_stats["GoalsScoredAvg"],
        away_stats["GoalsScoredAvg"],
        home_stats["GoalsConcededAvg"],
        away_stats["GoalsConcededAvg"],
        home_stats["GoalDiffAvg"] - away_stats["GoalDiffAvg"]
    ]]

    probs = model_result.predict_proba(features)[0]

    prob_home = probs[0]
    prob_draw = probs[1]
    prob_away = probs[2]

    prob_over = model_over.predict_proba(features)[0][1]
    prob_btts = model_btts.predict_proba(features)[0][1]

    value_home = prob_home * float(odds_home) - 1
    value_draw = prob_draw * float(odds_draw) - 1
    value_away = prob_away * float(odds_away) - 1

    confidence = max(prob_home, prob_draw, prob_away)

    return {
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "prob_over": round(prob_over, 3),
        "prob_btts": round(prob_btts, 3),
        "value_home": round(value_home, 3),
        "value_draw": round(value_draw, 3),
        "value_away": round(value_away, 3),
        "confidence": round(confidence, 3)
    }