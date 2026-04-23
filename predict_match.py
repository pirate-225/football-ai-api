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
    home_advantage = 1.15

    home_strength = (home_attack / max(away_def, 0.1)) * home_advantage
    away_strength = (away_attack / max(home_def, 0.1))

    # =========================
    # 🔥 FORME (léger)
    # =========================
    home_form = float(home.get("Form", 1.5))
    away_form = float(away.get("Form", 1.5))

    form_diff = (home_form - away_form) / 10

    home_strength *= (1 + form_diff)
    away_strength *= (1 - form_diff)

    # =========================
    # 🔥 DRAW
    # =========================
    diff = abs(home_strength - away_strength)

    prob_draw = 0.28 - (diff * 0.10)
    prob_draw = max(0.15, min(prob_draw, 0.30))

    # =========================
    # 🔥 PROBABILITÉS
    # =========================
    total_strength = home_strength + away_strength

    prob_home = home_strength / total_strength
    prob_away = away_strength / total_strength

    # 🔥 normalisation finale
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
    # 🔥 CONFIANCE
    # =========================
    confidence = max(prob_home, prob_draw, prob_away)

    return {
        "prediction": prediction,
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "confidence": round(confidence, 3)
    }