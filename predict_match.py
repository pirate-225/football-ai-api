import math
import numpy as np

def predict_match(home_team, away_team, odd_home, odd_draw, odd_away,
                  stats_home, stats_away, form_home, form_away,
                  shots_home, shots_away,
                  pos_home, pos_away,
                  xg_home, xg_away):

    if stats_home is None or stats_away is None:
        return None

    # =========================
    # 🔥 STATS API
    # =========================
    home_attack = stats_home["attack"] * 0.7 + form_home["attack"] * 0.3
    away_attack = stats_away["attack"] * 0.7 + form_away["attack"] * 0.3

    home_def = stats_home["defense"]
    away_def = stats_away["defense"]

    # =========================
    # 🔥 FORCE
    # =========================
    home_advantage = 1.15

    home_strength = (home_attack / max(away_def, 0.1)) * home_advantage
    away_strength = (away_attack / max(home_def, 0.1))

    # 🔥 AMPLIFICATION DES ÉCARTS (TRÈS IMPORTANT)
    home_strength = home_strength ** 1.5
    away_strength = away_strength ** 1.5

    # 🔥 ELO SIMPLE
    elo_home = stats_home["attack"] * 100
    elo_away = stats_away["attack"] * 100

    elo_diff = elo_home - elo_away

    home_strength *= (1 + elo_diff * 0.001)
    away_strength *= (1 - elo_diff * 0.001)

    # 🔥 impact tirs
    home_strength *= (1 + (shots_home - shots_away) * 0.04)
    away_strength *= (1 + (shots_away - shots_home) * 0.04)

    # 🔥 impact possession (léger)
    home_strength *= (1 + (pos_home - pos_away) * 0.002)
    away_strength *= (1 + (pos_away - pos_home) * 0.002)

    home_strength *= (1 + (shots_home - shots_away) * 0.04)
    away_strength *= (1 + (shots_away - shots_home) * 0.04)

    # =========================
    # 🔥 xG
    # =========================
    league_avg_goals = 2.6

    lambda_home = home_strength * 1.3
    lambda_away = away_strength * 1.1

    # 🔥 boost xG API
    lambda_home = (lambda_home + xg_home) / 2
    lambda_away = (lambda_away + xg_away) / 2

    # 🔥 xG basé sur tirs
    lambda_home *= (1 + shots_home * 0.03)
    lambda_away *= (1 + shots_away * 0.03)

    # normalisation
    scale = league_avg_goals / (lambda_home + lambda_away)
    lambda_home *= scale
    lambda_away *= scale

    # =========================
    # 🔥 POISSON
    # =========================
    def poisson_prob(lmbda, k):
        return (np.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

    max_goals = 6

    prob_home = 0
    prob_draw = 0
    prob_away = 0

    prob_over25 = 0
    prob_btts = 0

    for i in range(max_goals + 1):
        for j in range(max_goals + 1):

            p = poisson_prob(lambda_home, i) * poisson_prob(lambda_away, j)

            if i > j:
                prob_home += p
            elif i == j:
                prob_draw += p
            else:
                prob_away += p

            if (i + j) > 2:
                prob_over25 += p

            if i > 0 and j > 0:
                prob_btts += p

    total = prob_home + prob_draw + prob_away

    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 boost favoris
    prob_home = prob_home ** 1.2
    prob_away = prob_away ** 1.2

    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # =========================
    # 🔥 PREDICTION
    # =========================
    if prob_home > prob_away and prob_home > prob_draw:
        prediction = "HOME"
    elif prob_away > prob_home and prob_away > prob_draw:
        prediction = "AWAY"
    else:
        prediction = "DRAW"

    confidence = abs(prob_home - prob_away)

    return {
        "xg_home": round(lambda_home, 2),
        "xg_away": round(lambda_away, 2),
        "prediction": prediction,
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "confidence": round(confidence, 3),
        "over25": round(prob_over25, 3),
        "btts": round(prob_btts, 3),
    }