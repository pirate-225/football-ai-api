import pandas as pd

teams = pd.read_csv("data_processed/team_stats.csv")

def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    home = teams[teams["Team"] == home_team].iloc[0]
    away = teams[teams["Team"] == away_team].iloc[0]

    # 🔥 1. BASE = BOOKMAKER (TRÈS IMPORTANT)
    imp_home = 1 / float(odd_home)
    imp_draw = 1 / float(odd_draw)
    imp_away = 1 / float(odd_away)

    total_imp = imp_home + imp_draw + imp_away

    prob_home = imp_home / total_imp
    prob_draw = imp_draw / total_imp
    prob_away = imp_away / total_imp

    # 🔥 2. AJUSTEMENT AVEC TES DATA
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

    # 🔥 petit ajustement (clé du système)
    adjustment = diff * 0.05

    prob_home += adjustment
    prob_away -= adjustment

    # 🔥 re-normalisation
    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 OVER
    avg_goals = home["GoalsScoredAvg"] + away["GoalsScoredAvg"]
    prob_over = min(0.75, avg_goals / 3)

    # 🔥 BTTS
    prob_btts = (
        (1 - home["FailToScoreRate"]) *
        (1 - away["FailToScoreRate"])
    )

    # 🔥 EDGE (maintenant logique)
    edge_home = prob_home - imp_home
    edge_draw = prob_draw - imp_draw
    edge_away = prob_away - imp_away

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