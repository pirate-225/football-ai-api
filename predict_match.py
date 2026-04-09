import pandas as pd

teams = pd.read_csv("data_processed/team_stats.csv")

def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    home = teams[teams["Team"] == home_team].iloc[0]
    away = teams[teams["Team"] == away_team].iloc[0]

    # 🔥 FORCE RÉELLE (TRÈS IMPORTANT)
    home_strength = (
        home["PPG"] * 0.5 +
        home["HomePPG"] * 0.3 +
        home["Form"] * 0.2
    )

    away_strength = (
        away["PPG"] * 0.5 +
        away["AwayPPG"] * 0.3 +
        away["Form"] * 0.2
    )

    # 🔥 AVANTAGE DOMICILE
    home_strength *= 1.10

    # 🔥 NORMALISATION
    total = home_strength + away_strength

    prob_home = home_strength / total
    prob_away = away_strength / total

    # 🔥 DRAW réaliste
    prob_draw = 0.25 - abs(prob_home - prob_away) * 0.2
    prob_draw = max(0.15, prob_draw)

    # 🔥 NORMALISATION FINALE
    s = prob_home + prob_draw + prob_away
    prob_home /= s
    prob_draw /= s
    prob_away /= s

    # 🔥 OVER LOGIQUE
    avg_goals = home["GoalsScoredAvg"] + away["GoalsScoredAvg"]
    prob_over = min(0.75, avg_goals / 3)

    # 🔥 BTTS LOGIQUE
    prob_btts = (
        (1 - home["FailToScoreRate"]) *
        (1 - away["FailToScoreRate"])
    )

    # 🔥 EDGE CORRECT
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