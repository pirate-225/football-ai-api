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

    home_form = home["Form"]
    away_form = away["Form"]

    home_attack = home["GoalsScoredAvg"]
    away_attack = away["GoalsScoredAvg"]

    home_defense = home["GoalsConcededAvg"]
    away_defense = away["GoalsConcededAvg"]

    home_exp = home["MatchesPlayed"]
    away_exp = away["MatchesPlayed"]

    # 🔥 FEATURES IDENTIQUES AU TRAINING
    ppg_diff = home_ppg - away_ppg
    form_diff = home_form - away_form
    attack_diff = home_attack - away_attack
    defense_diff = home_defense - away_defense
    exp_diff = home_exp - away_exp

    strength_home = home_ppg * 0.7 + home_attack * 0.3
    strength_away = away_ppg * 0.7 + away_attack * 0.3
    strength_diff = strength_home - strength_away

    X = [[
        home_ppg,
        away_ppg,
        ppg_diff,
        form_diff,
        attack_diff,
        defense_diff,
        strength_diff,
        exp_diff
    ]]

    probs = model_result.predict_proba(X)[0]

    prob_home = probs[0]
    prob_draw = probs[1]
    prob_away = probs[2]

    prob_over = model_over.predict_proba(X)[0][1]
    prob_btts = model_btts.predict_proba(X)[0][1]

    # 🔥 EDGE
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