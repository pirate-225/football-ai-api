import pandas as pd
from api_football import get_team_data

teams = pd.read_csv("data_processed/team_stats.csv")


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    home = teams[teams["Team"] == home_team]
    away = teams[teams["Team"] == away_team]

    if home.empty or away.empty:
        return None

    home = home.iloc[0]
    away = away.iloc[0]

    # 🔥 API DATA
    home_api = get_team_data(home_team)
    away_api = get_team_data(away_team)

    # 🔥 fallback
    home_attack = home_api["attack"] if home_api else home["GoalsScoredAvg"]
    home_defense = home_api["defense"] if home_api else home["GoalsConcededAvg"]
    home_form = home_api["form"] if home_api else 0.5
    home_injuries = home_api["injuries"] if home_api else 0

    away_attack = away_api["attack"] if away_api else away["GoalsScoredAvg"]
    away_defense = away_api["defense"] if away_api else away["GoalsConcededAvg"]
    away_form = away_api["form"] if away_api else 0.5
    away_injuries = away_api["injuries"] if away_api else 0

    # 🔥 MODEL PRO
    home_strength = (
        home["PPG"] * 0.4 +
        home_attack * 0.25 -
        home_defense * 0.15 +
        home_form * 0.15 -
        home_injuries * 0.05
    ) + 0.3

    away_strength = (
        away["PPG"] * 0.4 +
        away_attack * 0.25 -
        away_defense * 0.15 +
        away_form * 0.15 -
        away_injuries * 0.05
    )

    total = home_strength + away_strength

    prob_home = home_strength / total
    prob_away = away_strength / total
    prob_draw = max(0.15, 1 - (prob_home + prob_away))

    # 🔥 bookmaker
    imp_home = 1 / float(odd_home)
    imp_draw = 1 / float(odd_draw)
    imp_away = 1 / float(odd_away)

    total_imp = imp_home + imp_draw + imp_away

    imp_home /= total_imp
    imp_draw /= total_imp
    imp_away /= total_imp

    return {
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "edge_home": round(prob_home - imp_home, 3),
        "edge_draw": round(prob_draw - imp_draw, 3),
        "edge_away": round(prob_away - imp_away, 3),
        "confidence": round(max(prob_home, prob_away), 3)
    }