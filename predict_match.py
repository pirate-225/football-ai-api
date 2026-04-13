import pandas as pd
from api_football import get_team_last_matches

teams = pd.read_csv("data_processed/team_stats.csv")


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    home_df = teams[teams["Team"] == home_team]
    away_df = teams[teams["Team"] == away_team]

    if home_df.empty or away_df.empty:
        return None

    home = home_df.iloc[0]
    away = away_df.iloc[0]

    # 🔥 API FORM
    home_form = get_team_last_matches(home_team)
    away_form = get_team_last_matches(away_team)

    # fallback si API fail
    if home_form:
        home_attack = home_form["scored"]
        home_defense = home_form["conceded"]
    else:
        home_attack = home["GoalsScoredAvg"]
        home_defense = home["GoalsConcededAvg"]

    if away_form:
        away_attack = away_form["scored"]
        away_defense = away_form["conceded"]
    else:
        away_attack = away["GoalsScoredAvg"]
        away_defense = away["GoalsConcededAvg"]

    # 🔥 FORCE MIX
    home_strength = (home["PPG"] * 0.5 + home_attack * 0.3 - home_defense * 0.2)
    away_strength = (away["PPG"] * 0.5 + away_attack * 0.3 - away_defense * 0.2)

    # 🔥 avantage domicile
    home_strength += 0.3

    total = home_strength + away_strength

    prob_home = home_strength / total
    prob_away = away_strength / total
    prob_draw = 1 - (prob_home + prob_away)

    # 🔥 bookmaker
    imp_home = 1 / float(odd_home)
    imp_draw = 1 / float(odd_draw)
    imp_away = 1 / float(odd_away)

    total_imp = imp_home + imp_draw + imp_away
    imp_home /= total_imp
    imp_draw /= total_imp
    imp_away /= total_imp

    edge_home = prob_home - imp_home
    edge_draw = prob_draw - imp_draw
    edge_away = prob_away - imp_away

    return {
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "edge_home": round(edge_home, 3),
        "edge_draw": round(edge_draw, 3),
        "edge_away": round(edge_away, 3),
        "confidence": round(max(prob_home, prob_away), 3)
    }