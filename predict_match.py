import pandas as pd
import joblib

team_stats = pd.read_csv("data_processed/team_stats.csv")

model_result = joblib.load("models/model_result.pkl")
model_over = joblib.load("models/model_over.pkl")
model_btts = joblib.load("models/model_btts.pkl")

def predict_match(home_team, away_team, odds_home, odds_draw, odds_away):

    home = team_stats[team_stats["Team"] == home_team].iloc[0]
    away = team_stats[team_stats["Team"] == away_team].iloc[0]

    home_ppg = home["PointsPerGame"]
    away_ppg = away["PointsPerGame"]

    home_goal_diff = home["GoalDiff"]
    away_goal_diff = away["GoalDiff"]

    home_form = home["Form"]
    away_form = away["Form"]

    elo_home = home["Elo"]
    elo_away = away["Elo"]

    position_home = home["Position"]
    position_away = away["Position"]

    features = [[
        home_ppg,
        away_ppg,
        home_ppg - away_ppg,
        home_goal_diff - away_goal_diff,
        position_home - position_away,
        elo_home - elo_away,
        home_form - away_form
    ]]

    probs = model_result.predict_proba(features)[0]

    prob_home = probs[0]
    prob_draw = probs[1]
    prob_away = probs[2]

    prob_over = model_over.predict_proba(features)[0][1]
    prob_btts = model_btts.predict_proba(features)[0][1]

    # Bookmaker probabilities
    book_home = 1 / float(odds_home)
    book_draw = 1 / float(odds_draw)
    book_away = 1 / float(odds_away)

    edge_home = prob_home - book_home
    edge_draw = prob_draw - book_draw
    edge_away = prob_away - book_away

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