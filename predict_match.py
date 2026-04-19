import pandas as pd
import numpy as np

try:
    injuries = pd.read_csv("data_processed/injuries.csv")
except:
    injuries = pd.DataFrame()

# 🔥 chargement données
team_data = pd.read_csv("data_processed/team_stats.csv")

# 🔥 standings safe
try:
    standings = pd.read_csv("data_processed/standings.csv")
except:
    standings = pd.DataFrame()


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    try:
        home = team_data.loc[team_data["Team"] == home_team].iloc[0]
        away = team_data.loc[team_data["Team"] == away_team].iloc[0]
    except:
        return None

    # 🔥 récupération données
    home_attack = float(home.get("HomeAttack", home["GoalsScoredAvg"]))
    away_attack = float(away.get("AwayAttack", away["GoalsScoredAvg"]))

    home_def = float(home["GoalsConcededAvg"])
    away_def = float(away["GoalsConcededAvg"])

    home_form = float(home.get("Form", 1.5))
    away_form = float(away.get("Form", 1.5))

    home_elo = float(home.get("ELO", 1000))
    away_elo = float(away.get("ELO", 1000))

    # 🔥 force de base
    home_strength = (home_attack / max(away_def, 0.1))
    away_strength = (away_attack / max(home_def, 0.1))

    # 🔥 impact forme
    form_diff = (home_form - away_form) / 8
    home_strength *= (1 + form_diff)
    away_strength *= (1 - form_diff)

    # 🔥 impact elo
    elo_diff = (home_elo - away_elo) / 600
    home_strength *= (1 + elo_diff)
    away_strength *= (1 - elo_diff)

    # 🔥 impact classement (IMPORTANT)
    home_rank = standings.loc[standings["Team"] == home_team]["Rank"]
    away_rank = standings.loc[standings["Team"] == away_team]["Rank"]

    if not home_rank.empty and not away_rank.empty:
        rank_diff = (away_rank.values[0] - home_rank.values[0]) / 35
        home_strength *= (1 + rank_diff)
        away_strength *= (1 - rank_diff)

    # 🔥 impact blessures
    if not injuries.empty:
        home_inj = injuries.loc[injuries["Team"] == home_team]["Injuries"]
        away_inj = injuries.loc[injuries["Team"] == away_team]["Injuries"]

        if not home_inj.empty:
            home_strength *= (1 - min(home_inj.values[0] * 0.03, 0.15))

        if not away_inj.empty:
            away_strength *= (1 - min(away_inj.values[0] * 0.03, 0.15))

    # 🔥 éviter valeurs extrêmes
    home_strength = max(home_strength, 0.01)
    away_strength = max(away_strength, 0.01)

    # 🔥 probabilités brutes
    total = home_strength + away_strength
    prob_home = home_strength / total
    prob_away = away_strength / total

    # 🔥 draw réaliste
    prob_draw = 1 - abs(prob_home - prob_away)
    prob_draw *= 0.25

    # 🔥 normalisation finale
    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 éviter extrêmes irréalistes
    prob_home = min(max(prob_home, 0.05), 0.85)
    prob_away = min(max(prob_away, 0.05), 0.85)

    # 🔥 renormalisation après clamp
    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 calibration globale (CRUCIAL)
    prob_home = prob_home * 0.9 + 0.05
    prob_away = prob_away * 0.9 + 0.05

    # 🔥 correction favoris moyens (CRUCIAL)
    if 0.55 < prob_home < 0.75:
        prob_home *= 0.9

    if 0.55 < prob_away < 0.75:
        prob_away *= 0.9

    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 renormalisation après calibration
    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 over / btts
    goal_expectation = (home_attack + away_attack) / 2

    prob_over = sigmoid(goal_expectation - 2.4)
    prob_btts = sigmoid((home_attack * away_attack) - 1.2)

    # 🔥 signal marché (simple)
    market_confidence = (1/odd_home + 1/odd_away)

    if market_confidence > 1.1:
        prob_home *= 0.95
        prob_away *= 0.95

    # 🔥 renormalisation après marché
    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 edge
    implied_home = 1 / odd_home
    implied_draw = 1 / odd_draw
    implied_away = 1 / odd_away

    # 🔥 calibration (IMPORTANT)
    confidence_factor = 0.85

    edge_home = (prob_home * confidence_factor) - implied_home
    edge_draw = (prob_draw * confidence_factor) - implied_draw
    edge_away = (prob_away * confidence_factor) - implied_away

    return {
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "prob_over": round(prob_over, 3),
        "prob_btts": round(prob_btts, 3),
        "edge_home": round(edge_home, 3),
        "edge_draw": round(edge_draw, 3),
        "edge_away": round(edge_away, 3)
    }