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


team_data = pd.read_csv("data_processed/team_stats.csv")


def predict_match(
    home, away,
    odd_home, odd_draw, odd_away,
    xg_home_stats, xg_away_stats,
    shots_home, shots_away,
    pos_home, pos_away,
    h2h_home, h2h_away
):

    def normalize(name):
        return str(name).lower().strip()

    def find_team(name):
        name = normalize(name)

        for _, row in team_data.iterrows():
            team = normalize(row["Team"])
            if name == team:
                return row

        for _, row in team_data.iterrows():
            team = normalize(row["Team"])
            if name in team or team in name:
                return row

        return None

    home_row = find_team(home)
    away_row = find_team(away)

    if home_row is None or away_row is None:
        return None

    # 🔥 BASE STATS
    home_attack = float(home_row["GoalsScoredAvg"])
    home_def = float(home_row["GoalsConcededAvg"])
    away_attack = float(away_row["GoalsScoredAvg"])
    away_def = float(away_row["GoalsConcededAvg"])

    # 🔥 FORM
    try:
        home_form = get_recent_form(home)
        away_form = get_recent_form(away)
    except:
        home_form = 1.5
        away_form = 1.5

    # 🔥 SECURISATION DATA
    try:
        shots_home = float(shots_home)
        shots_away = float(shots_away)
    except:
        shots_home = 5
        shots_away = 5

    def to_float(x, default=1.2):
        try:
            return float(x)
        except:
            return default

    xg_home_for = to_float(xg_home_stats.get("xg_for"))
    xg_home_against = to_float(xg_home_stats.get("xg_against"))

    xg_away_for = to_float(xg_away_stats.get("xg_for"))
    xg_away_against = to_float(xg_away_stats.get("xg_against"))

    # 🔥 ÉQUILIBRAGE SI UN SEUL XG EST RÉEL (ROBUSTE)
    if abs(xg_home_for - 1.2) < 0.01 and xg_away_for > 1.25:
        xg_home_for = xg_away_for * 0.85

    if abs(xg_away_for - 1.2) < 0.01 and xg_home_for > 1.25:
        xg_away_for = xg_home_for * 0.85

    # 🔥 IMPACT RÉEL DES TIRS
    shots_factor_home = (shots_home / 10)
    shots_factor_away = (shots_away / 10)

    # 🔥 NOUVEAU CALCUL PLUS INDÉPENDANT

    attack_home = (
        xg_home_for * 0.5 +
        home_attack * 0.3 +
        shots_home * 0.02
    )

    attack_away = (
        xg_away_for * 0.5 +
        away_attack * 0.3 +
        shots_away * 0.02
    )

    # ⚠️ IMPORTANT → défini AVANT utilisation
    defense_home = xg_home_against
    defense_away = xg_away_against

    home_adv = 1.12

    lambda_home = (attack_home / max(defense_away, 0.1)) * home_adv
    lambda_away = (attack_away / max(defense_home, 0.1))

    # 🔥 BOOST CONTEXTE (très important)
    form_diff = (home_form - away_form) * 0.4
    form_diff = max(min(form_diff, 0.4), -0.4)

    lambda_home *= (1 + form_diff)
    lambda_away *= (1 - form_diff)

    lambda_home *= (1 + form_diff * 0.35)
    lambda_away *= (1 - form_diff * 0.35)

    # sécurité
    lambda_home = max(lambda_home, 0.3)
    lambda_away = max(lambda_away, 0.3)

    # 🔥 ANTI-FAVORI (équilibrage)
    diff = lambda_home - lambda_away

    if abs(diff) < 0.5:
        lambda_home *= 1.05
        lambda_away *= 1.05

    # 🔥 IMPACT POSSESSION (léger mais utile)
    pos_diff = (pos_home - pos_away) / 100

    lambda_home *= (1 + pos_diff * 0.3)
    lambda_away *= (1 - pos_diff * 0.3)

    # 🔥 DIFF NIVEAU SAFE
    diff = lambda_home - lambda_away
    diff = max(min(diff, 1), -1)

    lambda_home *= (1 + diff * 0.25)
    lambda_away *= (1 - diff * 0.25)

    # 🔥 FORM IMPACT (plus puissant mais contrôlé)
    form_diff = (home_form - away_form) * 0.5
    form_diff = max(min(form_diff, 0.5), -0.5)

    lambda_home *= (1 + form_diff)
    lambda_away *= (1 - form_diff)

    # 🔥 SECURITE
    lambda_home = max(lambda_home, 0.3)
    lambda_away = max(lambda_away, 0.3)

    # 🔥 NORMALISATION
    league_avg_goals = 2.6

    total_lambda = lambda_home + lambda_away

    if total_lambda > 0:
        scale = league_avg_goals / total_lambda

        # 🔥 très faible variation (clé)
        scale = max(min(scale, 1.05), 0.95)

        lambda_home *= scale
        lambda_away *= scale

    # 🔥 POISSON
    def poisson(lmbda, k):
        return (np.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

    prob_home = prob_draw = prob_away = 0

    for i in range(6):
        for j in range(6):
            p = poisson(lambda_home, i) * poisson(lambda_away, j)
            if i > j:
                prob_home += p
            elif i == j:
                prob_draw += p
            else:
                prob_away += p

    # 🔥 NORMALISATION
    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 FUSION SIMPLE ET STABLE (IMPORTANT)
    if odd_home > 0 and odd_draw > 0 and odd_away > 0:

        market_home = 1 / odd_home
        market_draw = 1 / odd_draw
        market_away = 1 / odd_away

        total_market = market_home + market_draw + market_away

        market_home /= total_market
        market_draw /= total_market
        market_away /= total_market

    # 🔥 MODE INDÉPENDANT
    # on NE mélange PAS avec les cotes
    pass

    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 PREDICTION VALUE
    if prob_home > prob_away and prob_home > prob_draw:
        prediction = "HOME"
    elif prob_away > prob_home and prob_away > prob_draw:
        prediction = "AWAY"
    else:
        prediction = "DRAW"

    confidence = abs(prob_home - prob_away)

    # =========================
    # 🔥 PROBA BOOKMAKER
    # =========================
    if odd_home > 0 and odd_draw > 0 and odd_away > 0:
        market_home = 1 / odd_home
        market_draw = 1 / odd_draw
        market_away = 1 / odd_away

        total_market = market_home + market_draw + market_away

        market_home /= total_market
        market_draw /= total_market
        market_away /= total_market
    else:
        market_home = market_draw = market_away = 0


    # =========================
    # 🔥 VALUE
    # =========================
    edge_home = prob_home - market_home
    edge_draw = prob_draw - market_draw
    edge_away = prob_away - market_away


    # =========================
    # 🔥 FILTRE VALUE (SAFE)
    # =========================
    # 🔥 FILTRE VALUE
    value_bet = None

    if edge_home > 0.08 and prob_home > 0.42:
        value_bet = "HOME"

    elif edge_away > 0.08 and prob_away > 0.42:
        value_bet = "AWAY"

    elif edge_draw > 0.08 and prob_draw > 0.30:
        value_bet = "DRAW"


    # 🔥 ANTI FAUX VALUE (À AJOUTER ICI)
    if abs(edge_home) < 0.01 and abs(edge_away) < 0.01:
        value_bet = None

    # 🔥 FILTRE CONFIANCE
    if confidence < 0.12:
        value_bet = None


    # 🔥 MATCHS PIÉGEUX
    if 0.40 < prob_home < 0.60 and 0.40 < prob_away < 0.60:
        value_bet = None

    # 🔥 NORMALISATION FINALE
    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 EDGE (temporaire neutre)
    edge_home = 0
    edge_away = 0
    edge_draw = 0

    # 🔥 OVER 2.5
    prob_over = 0
    for i in range(6):
        for j in range(6):
            if i + j > 2:
                prob_over += poisson(lambda_home, i) * poisson(lambda_away, j)

    over_25 = prob_over > 0.5

    return {
        "xg_home": round(lambda_home, 2),
        "xg_away": round(lambda_away, 2),
        "prediction": prediction,
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "confidence": round(confidence, 3),

        "value_bet": value_bet,

        "edge_home": round(edge_home, 3),
        "edge_draw": round(edge_draw, 3),
        "edge_away": round(edge_away, 3),

        "over_25": over_25,
        "prob_over": round(prob_over, 3),
    }