import math
import pandas as pd
import numpy as np
import requests

# 🔥 FORM LIVE
def get_recent_form(team_id):

    try:
        url = "https://v3.football.api-sports.io/fixtures"

        headers = {
            "x-apisports-key": "3b63a56a290a3bd3d4b00c5b232d37d3"
        }

        params = {
            "team": team_id,
            "last": 5
        }

        res = requests.get(
            url,
            headers=headers,
            params=params
        ).json()

        print("FORM API RESPONSE:", res)

        points = 0

        for f in res.get("response", []):

            home_id = f["teams"]["home"]["id"]
            away_id = f["teams"]["away"]["id"]

            gh = f["goals"]["home"]
            ga = f["goals"]["away"]

            if gh is None or ga is None:
                continue

            # 🔥 équipe joue à domicile
            if team_id == home_id:

                if gh > ga:
                    points += 3

                elif gh == ga:
                    points += 1

            # 🔥 équipe joue à l'extérieur
            else:

                if ga > gh:
                    points += 3

                elif gh == ga:
                    points += 1

        print("POINTS:", points)

        return points / 5

    except Exception as e:

        print("FORM ERROR:", e)

        return 1.5


team_data = pd.read_csv("data_processed/team_stats.csv")


def predict_match(
    home, away,
    odd_home, odd_draw, odd_away,
    xg_home_stats, xg_away_stats,
    shots_home, shots_away,
    pos_home, pos_away,
    h2h_home, h2h_away,
    home_id, away_id
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
        home_form = get_recent_form(home_id)
        away_form = get_recent_form(away_id)
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
    # =========================
    # 🔥 BASE OFFENSIVE / DEFENSIVE
    # =========================

    attack_home = (
        home_attack * 0.75 +
        xg_home_for * 0.25
    )

    attack_away = (
        away_attack * 0.75 +
        xg_away_for * 0.25
    )

    defense_home = (
        home_def * 0.75 +
        xg_home_against * 0.25
    )

    defense_away = (
        away_def * 0.75 +
        xg_away_against * 0.25
    )

    # =========================
    # 🔥 AVANTAGE DOMICILE
    # =========================

    home_adv = 1.10

    # =========================
    # 🔥 NOUVELLE FORMULE LAMBDA
    # =========================

    lambda_home = (
        attack_home * 0.65 +
        (2 - defense_away) * 0.35
    ) * home_adv

    lambda_away = (
        attack_away * 0.65 +
        (2 - defense_home) * 0.35
    )

    # =========================
    # 🔥 IMPACT FORME (LÉGER)
    # =========================

    form_diff = (home_form - away_form) * 0.12
    form_diff = max(min(form_diff, 0.15), -0.15)

    lambda_home *= (1 + form_diff)
    lambda_away *= (1 - form_diff)

    # =========================
    # 🔥 IMPACT POSSESSION
    # =========================

    if pos_home != 50 or pos_away != 50:

        pos_diff = (pos_home - pos_away) / 100

        lambda_home *= (1 + pos_diff * 0.10)
        lambda_away *= (1 - pos_diff * 0.10)

    # =========================
    # 🔥 IMPACT TIRS
    # =========================

    shots_total = shots_home + shots_away

    if shots_total > 24:
        lambda_home *= 1.08
        lambda_away *= 1.08

    elif shots_total < 18:
        lambda_home *= 0.92
        lambda_away *= 0.92

    # =========================
    # 🔥 LIMITES IMPORTANTES
    # =========================

    lambda_home = min(max(lambda_home, 0.4), 3.2)
    lambda_away = min(max(lambda_away, 0.4), 3.2)

    # =========================
    # 🔥 NORMALISATION DOUCE
    # =========================

    league_avg_goals = 2.7

    total_lambda = lambda_home + lambda_away

    if total_lambda > 0:

        scale = league_avg_goals / total_lambda

        scale = max(min(scale, 1.15), 0.85)

        lambda_home *= scale
        lambda_away *= scale

    print("===================================")
    print(home, "vs", away)

    print("XG HOME:", xg_home_for)
    print("XG AWAY:", xg_away_for)

    print("HOME ATTACK:", attack_home)
    print("AWAY ATTACK:", attack_away)

    print("HOME DEF:", defense_home)
    print("AWAY DEF:", defense_away)

    print("LAMBDA HOME:", lambda_home)
    print("LAMBDA AWAY:", lambda_away)

    print("SHOTS:", shots_home, shots_away)
    print("POSSESSION:", pos_home, pos_away)

    print("FORM:", home_form, away_form)

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

    # =========================
    # 🔥 FUSION LÉGÈRE BOOKMAKER
    # =========================

    if odd_home > 0 and odd_draw > 0 and odd_away > 0:

        market_home = 1 / odd_home
        market_draw = 1 / odd_draw
        market_away = 1 / odd_away

        total_market = market_home + market_draw + market_away

        market_home /= total_market
        market_draw /= total_market
        market_away /= total_market

        # 🔥 légère influence marché
        prob_home = prob_home * 0.85 + market_home * 0.15
        prob_draw = prob_draw * 0.85 + market_draw * 0.15
        prob_away = prob_away * 0.85 + market_away * 0.15

        # 🔥 renormalisation finale
        total = prob_home + prob_draw + prob_away

        prob_home /= total
        prob_draw /= total
        prob_away /= total

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