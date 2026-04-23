import pandas as pd
import numpy as np

# 🔥 DATA
team_data = pd.read_csv("data_processed/team_stats.csv")


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    try:
        home = team_data.loc[team_data["Team"] == home_team].iloc[0]
        away = team_data.loc[team_data["Team"] == away_team].iloc[0]
    except:
        return None

    # =========================
    # 🔥 BASE STATS
    # =========================
    home_attack = float(home["GoalsScoredAvg"])
    home_def = float(home["GoalsConcededAvg"])

    away_attack = float(away["GoalsScoredAvg"])
    away_def = float(away["GoalsConcededAvg"])

    # =========================
    # 🔥 FORCE DES ÉQUIPES
    # =========================
    home_strength = (home_attack / max(away_def, 0.1)) * 1.10  # avantage domicile
    away_strength = (away_attack / max(home_def, 0.1))

    # =========================
    # 🔥 PROBABILITÉS
    # =========================
    total = home_strength + away_strength

    prob_home = home_strength / total
    prob_away = away_strength / total

    # draw simple mais stable
    prob_draw = 1 - abs(prob_home - prob_away)
    prob_draw *= 0.25

    # normalisation
    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # =========================
    # 🔥 PRÉDICTION
    # =========================
    if prob_home > prob_away and prob_home > prob_draw:
        prediction = "HOME"
    elif prob_away > prob_home and prob_away > prob_draw:
        prediction = "AWAY"
    else:
        prediction = "DRAW"

    # =========================
    # 🔥 CONFIANCE SIMPLE
    # =========================
    confidence = max(prob_home, prob_draw, prob_away)

    return {
        "prediction": prediction,
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "confidence": round(confidence, 3)
    }