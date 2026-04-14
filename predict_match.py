import pandas as pd

teams = pd.read_csv("data_processed/team_stats.csv")


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    home = teams[teams["Team"] == home_team]
    away = teams[teams["Team"] == away_team]

    if home.empty or away.empty:
        return None

    home = home.iloc[0]
    away = away.iloc[0]

    # 🔥 modèle amélioré
    home_strength = (
        home["PPG"] * 0.6 +
        home["GoalsScoredAvg"] * 0.3 -
        home["GoalsConcededAvg"] * 0.1
    ) + 0.3

    away_strength = (
        away["PPG"] * 0.6 +
        away["GoalsScoredAvg"] * 0.3 -
        away["GoalsConcededAvg"] * 0.1
    )

    total = home_strength + away_strength

    prob_home = home_strength / total
    prob_away = away_strength / total
    prob_draw = max(0.15, 1 - (prob_home + prob_away))

    return {
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "confidence": round(max(prob_home, prob_away), 3)
    }