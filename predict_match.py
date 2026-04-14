import pandas as pd

teams = pd.read_csv("data_processed/team_stats.csv")


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    home = teams[teams["Team"] == home_team]
    away = teams[teams["Team"] == away_team]

    if home.empty or away.empty:
        return None

    home = home.iloc[0]
    away = away.iloc[0]

    # 🔥 FORCE ÉQUIPE
    home_strength = (
        home["PPG"] * 0.7 +
        home["GoalsScoredAvg"] * 0.2 -
        home["GoalsConcededAvg"] * 0.1
    ) + 0.35

    away_strength = (
        away["PPG"] * 0.7 +
        away["GoalsScoredAvg"] * 0.2 -
        away["GoalsConcededAvg"] * 0.1
    )

    total = home_strength + away_strength

    prob_home = home_strength / total
    prob_away = away_strength / total
    prob_draw = max(0.18, 1 - (prob_home + prob_away))

    # 🔥 xG SIMPLE (clé pour over/btts)
    home_xg = (home["GoalsScoredAvg"] + away["GoalsConcededAvg"]) / 2
    away_xg = (away["GoalsScoredAvg"] + home["GoalsConcededAvg"]) / 2

    total_xg = home_xg + away_xg

    # 🔥 OVER 2.5 (approximation rapide)
    prob_over = min(0.85, total_xg / 2.8)

    # 🔥 BTTS (approximation logique)
    prob_btts = min(0.85, (home_xg * away_xg) / 2.5)

    # 🔥 bookmaker
    imp_home = 1 / float(odd_home)
    imp_draw = 1 / float(odd_draw)
    imp_away = 1 / float(odd_away)

    total_imp = imp_home + imp_draw + imp_away

    imp_home /= total_imp
    imp_draw /= total_imp
    imp_away /= total_imp

    # 🔥 EDGE
    edge_home = prob_home - imp_home
    edge_draw = prob_draw - imp_draw
    edge_away = prob_away - imp_away

    return {
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "prob_over": round(prob_over, 3),
        "prob_btts": round(prob_btts, 3),
        "edge_home": round(edge_home, 3),
        "edge_draw": round(edge_draw, 3),
        "edge_away": round(edge_away, 3),
        "confidence": round(max(prob_home, prob_away), 3)
    }