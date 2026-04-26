import math
import pandas as pd
import numpy as np
import requests

# 🔥 FORM LIVE
def get_recent_form(team_name):
    try:
        url = "https://v3.football.api-sports.io/fixtures"
        headers = {"x-apisports-key": "3b63a56a290a3bd3d4b00c5b232d37d3"}

        params = {"team": team_name, "last": 5}

        res = requests.get(url, headers=headers, params=params).json()

        points = 0

        for f in res.get("response", []):
            home = f["teams"]["home"]["name"]
            away = f["teams"]["away"]["name"]

            gh = f["goals"]["home"]
            ga = f["goals"]["away"]

            if gh is None:
                continue

            if team_name == home:
                if gh > ga:
                    points += 3
                elif gh == ga:
                    points += 1
            else:
                if ga > gh:
                    points += 3
                elif gh == ga:
                    points += 1

        return points / 5

    except:
        return 1.5


# 🔥 DATA
team_data = pd.read_csv("data_processed/team_stats.csv")


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    # =========================
    # 🔥 MATCHING ÉQUIPES
    # =========================
    def normalize(name):
        return str(name).lower().strip()

    def find_team(name):
        name = normalize(name)

        for _, row in team_data.iterrows():
            team = normalize(row["Team"])
            if name == team:
                return row

        # fallback
        for _, row in team_data.iterrows():
            team = normalize(row["Team"])
            if name in team or team in name:
                return row

        return None

    home = find_team(home_team)
    away = find_team(away_team)

    if home is None or away is None:
        return None

    # =========================
    # 🔥 BASE STATS
    # =========================
    home_attack = float(home["GoalsScoredAvg"])
    home_def = float(home["GoalsConcededAvg"])

    away_attack = float(away["GoalsScoredAvg"])
    away_def = float(away["GoalsConcededAvg"])

    # =========================
    # 🔥 FORM
    # =========================
    try:
        home_form = get_recent_form(home_team)
        away_form = get_recent_form(away_team)
    except:
        home_form = 1.5
        away_form = 1.5

    # =========================
    # 🔥 FORCE
    # =========================
    home_advantage = 1.2

    alpha = 0.75
    beta = 0.25

    home_form_factor = (home_form - 1.5) * 0.4
    away_form_factor = (away_form - 1.5) * 0.4

    home_strength = (
        (home_attack / max(away_def, 0.1)) * alpha +
        home_form_factor * beta
    ) * home_advantage

    away_strength = (
        (away_attack / max(home_def, 0.1)) * alpha +
        away_form_factor * beta
    )

    # 🔥 amplification des écarts (clé)
    home_strength = home_strength ** 1.3
    away_strength = away_strength ** 1.3

    # =========================
    # 🔥 xG RÉALISTES
    # =========================
    league_avg_goals = 2.6

    lambda_home = home_strength * np.random.uniform(1.2, 1.8)
    lambda_away = away_strength * np.random.uniform(1.0, 1.6)

    lambda_home = max(lambda_home, 0.8)
    lambda_away = max(lambda_away, 0.8)

    over = lambda_home + lambda_away

    lambda_home *= np.random.uniform(0.8, 1.3)
    lambda_away *= np.random.uniform(0.8, 1.3)

    scale = league_avg_goals / (lambda_home + lambda_away)

    lambda_home *= scale
    lambda_away *= scale

    # 🔥 DIFFÉRENCE DE NIVEAU
    strength_diff = home_strength - away_strength

    lambda_home *= (1 + strength_diff * 0.3)
    lambda_away *= (1 - strength_diff * 0.3)

    # 🔥 variance réaliste
    lambda_home *= np.random.uniform(0.85, 1.35)
    lambda_away *= np.random.uniform(0.85, 1.35)

    # =========================
    # 🔥 POISSON
    # =========================
    def poisson_prob(lmbda, k):
        return (np.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

    max_goals = 6

    prob_home = 0
    prob_draw = 0
    prob_away = 0

    best_score = (0, 0)
    best_prob = 0

    for i in range(max_goals + 1):
        for j in range(max_goals + 1):

            p = poisson_prob(lambda_home, i) * poisson_prob(lambda_away, j)

            if p > best_prob:
                best_prob = p
                best_score = (i, j)

            if i > j:
                prob_home += p
            elif i == j:
                prob_draw += p
            else:
                prob_away += p

    score_home, score_away = best_score

    # =========================
    # 🔥 NORMALISATION
    # =========================
    total = prob_home + prob_draw + prob_away

    if total == 0:
        prob_home = 0.33
        prob_draw = 0.34
        prob_away = 0.33
    else:
        prob_home /= total
        prob_draw /= total
        prob_away /= total

    # 🔥 calibration douce
    prob_home = prob_home * 0.9 + 0.05
    prob_away = prob_away * 0.9 + 0.05

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
    confidence = abs(prob_home - prob_away)

    dominance = abs(prob_home - prob_away)

    return {
    "xg_home": round(lambda_home, 2),
    "xg_away": round(lambda_away, 2),
    "prediction": prediction,
    "prob_home": round(prob_home, 3),
    "prob_draw": round(prob_draw, 3),
    "prob_away": round(prob_away, 3),
    "confidence": round(confidence, 3),
    "score": f"{score_home}-{score_away}",

    # 🔥 AJOUTS
    "over": round(over, 2),
    "dominance": round(dominance, 2),
}