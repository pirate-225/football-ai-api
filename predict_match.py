import pandas as pd
import joblib

teams = pd.read_csv("data_processed/team_stats.csv")

model_result = joblib.load("models/model_result.pkl")
model_over = joblib.load("models/model_over.pkl")
model_btts = joblib.load("models/model_btts.pkl")

def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    home = teams[teams["Team"] == home_team].iloc[0]
    away = teams[teams["Team"] == away_team].iloc[0]

    X = [[
        home["PPG"] - away["PPG"],
        home["HomePPG"] - away["AwayPPG"],
        home["Form"] - away["Form"],
        home["GoalsScoredAvg"] - away["GoalsScoredAvg"],
        home["GoalsConcededAvg"] - away["GoalsConcededAvg"],
        home["CleanSheetRate"] - away["CleanSheetRate"],
        home["FailToScoreRate"] - away["FailToScoreRate"],
        home["ELO"] - away["ELO"],
        home["MatchesPlayed"] - away["MatchesPlayed"],
        0  # league_diff par défaut si absent
    ]]

    probs = model_result.predict_proba(X)[0]
    # 🔥 inversion possible (test)
    prob_home = probs[2]
    prob_draw = probs[1]
    prob_away = probs[0]

    prob_over = model_over.predict_proba(X)[0][1]
    prob_btts = model_btts.predict_proba(X)[0][1]

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