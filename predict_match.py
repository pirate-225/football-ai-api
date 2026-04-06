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

    # Calibration simple Over / BTTS
    prob_over = min(max(prob_over, 0.05), 0.95)
    prob_btts = min(max(prob_btts, 0.05), 0.95)

    # Bookmaker probabilities
    book_home = 1 / float(odds_home)
    book_draw = 1 / float(odds_draw)
    book_away = 1 / float(odds_away)

    # Edge
    edge_home = prob_home - book_home
    edge_draw = prob_draw - book_draw
    edge_away = prob_away - book_away

    confidence = max(prob_home, prob_draw, prob_away)

    bet_home = "YES" if edge_home > 0.05 else "NO"
    bet_draw = "YES" if edge_draw > 0.05 else "NO"
    bet_away = "YES" if edge_away > 0.05 else "NO"

    return {
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),

        "prob_over": round(prob_over, 3),
        "prob_btts": round(prob_btts, 3),

        "book_home": round(book_home, 3),
        "book_draw": round(book_draw, 3),
        "book_away": round(book_away, 3),

        "edge_home": round(edge_home, 3),
        "edge_draw": round(edge_draw, 3),
        "edge_away": round(edge_away, 3),

        "bet_home": bet_home,
        "bet_draw": bet_draw,
        "bet_away": bet_away,

        "confidence": round(confidence, 3)
    }