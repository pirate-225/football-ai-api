import pandas as pd

teams = pd.read_csv("data_processed/team_stats.csv")


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    home_df = teams[teams["Team"] == home_team]
    away_df = teams[teams["Team"] == away_team]

    if home_df.empty or away_df.empty:
        return None

    home = home_df.iloc[0]
    away = away_df.iloc[0]

    # 🔥 FORCE RÉELLE DES ÉQUIPES
    strength_home = (
        home["PPG"] * 0.4 +
        home["HomePPG"] * 0.3 +
        home["GoalsScoredAvg"] * 0.2 -
        home["GoalsConcededAvg"] * 0.1
    )

    strength_away = (
        away["PPG"] * 0.4 +
        away["AwayPPG"] * 0.3 +
        away["GoalsScoredAvg"] * 0.2 -
        away["GoalsConcededAvg"] * 0.1
    )

    total = strength_home + strength_away

    prob_home = strength_home / total
    prob_away = strength_away / total
    prob_draw = 1 - (prob_home + prob_away)

    # 🔥 OVER basé sur attaque
    prob_over = min(0.85, (home["GoalsScoredAvg"] + away["GoalsScoredAvg"]) / 2.5)

    # 🔥 BTTS basé sur scoring + défense
    prob_btts = (
        (home["GoalsScoredAvg"] > 1.2) *
        (away["GoalsScoredAvg"] > 1.2)
    ) * 0.7 + 0.3

    # 🔥 EDGE RÉEL
    imp_home = 1 / float(odd_home)
    imp_away = 1 / float(odd_away)

    edge_home = prob_home - imp_home
    edge_away = prob_away - imp_away

    confidence = max(prob_home, prob_away)

    return {
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "prob_over": round(prob_over, 3),
        "prob_btts": round(prob_btts, 3),
        "edge_home": round(edge_home, 3),
        "edge_away": round(edge_away, 3),
        "confidence": round(confidence, 3)
    }