import pandas as pd
import numpy as np
import requests

# 🔥 FORM LIVE
def get_recent_form(team_name):
    try:
        url = "https://v3.football.api-sports.io/fixtures"
        headers = {"x-apisports-key": "3b63a56a290a3bd3d4b00c5b232d37d3"}

        params = {"team": team_name, "last": 5}
        res = requests.get(url, headers=headers, params=params, timeout=5).json()

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
try:
    injuries = pd.read_csv("data_processed/injuries.csv")
except:
    injuries = pd.DataFrame()

team_data = pd.read_csv("data_processed/team_stats.csv")

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

    # 🔥 stats
    home_attack = float(home.get("HomeAttack", home["GoalsScoredAvg"]))
    away_attack = float(away.get("AwayAttack", away["GoalsScoredAvg"]))
    home_def = float(home["GoalsConcededAvg"])
    away_def = float(away["GoalsConcededAvg"])

    # 🔥 FORM
    try:
        home_form = get_recent_form(home_team)
        away_form = get_recent_form(away_team)
    except:
        home_form = float(home.get("Form", 1.5))
        away_form = float(away.get("Form", 1.5))

    home_elo = float(home.get("ELO", 1000))
    away_elo = float(away.get("ELO", 1000))

    # 🔥 force
    home_strength = home_attack / max(away_def, 0.1)
    away_strength = away_attack / max(home_def, 0.1)

    # 🔥 forme (réduite pour éviter biais)
    form_diff = (home_form - away_form) / 5
    home_strength *= (1 + form_diff)
    away_strength *= (1 - form_diff)

    # 🔥 elo (réduit)
    elo_diff = (home_elo - away_elo) / 400
    home_strength *= (1 + elo_diff)
    away_strength *= (1 - elo_diff)

    # 🔥 classement
    home_rank = standings.loc[standings["Team"] == home_team]["Rank"]
    away_rank = standings.loc[standings["Team"] == away_team]["Rank"]

    if not home_rank.empty and not away_rank.empty:
        rank_diff = (away_rank.values[0] - home_rank.values[0]) / 30
        home_strength *= (1 + rank_diff)
        away_strength *= (1 - rank_diff)

    # 🔥 blessures
    if not injuries.empty:
        home_inj = injuries.loc[injuries["Team"] == home_team]["Injuries"]
        away_inj = injuries.loc[injuries["Team"] == away_team]["Injuries"]

        if not home_inj.empty:
            home_strength *= (1 - min(home_inj.values[0] * 0.03, 0.15))
        if not away_inj.empty:
            away_strength *= (1 - min(away_inj.values[0] * 0.03, 0.15))

    # 🔥 probas
    home_strength = max(home_strength, 0.01)
    away_strength = max(away_strength, 0.01)

    total = home_strength + away_strength
    prob_home = home_strength / total
    prob_away = away_strength / total

    prob_draw = (1 - abs(prob_home - prob_away)) * 0.25

    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 calibration réaliste
    prob_home = prob_home * 0.9 + 0.05
    prob_away = prob_away * 0.9 + 0.05

    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 éviter probas trop faibles
    prob_home = max(prob_home, 0.05)
    prob_away = max(prob_away, 0.05)

    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 over / btts
    # 🔥 expected goals réalistes
    lambda_home = home_attack * (away_def + 1) / 2
    lambda_away = away_attack * (home_def + 1) / 2

    expected_goals = lambda_home + lambda_away

    # 🔥 probabilité Over 2.5 (approximation Poisson)
    prob_over = 1 - (
        np.exp(-expected_goals) * (
            1 + expected_goals + (expected_goals**2)/2
        )
    )
    prob_btts = sigmoid((home_attack * away_attack) - 1.2)

    # 🔥 marché
    implied_home = 1 / odd_home
    implied_draw = 1 / odd_draw
    implied_away = 1 / odd_away

    # 🔥 edge
    confidence_factor = 0.75
    edge_home = (prob_home * confidence_factor) - implied_home
    edge_draw = (prob_draw * confidence_factor) - implied_draw
    edge_away = (prob_away * confidence_factor) - implied_away

    # 🔥 ignorer faux edges
    if max(edge_home, edge_away) < 0.03:
        return None

    # ==============================
    # 🔥 FILTRES INTELLIGENTS
    # ==============================

    # ❌ match trop équilibré
    if abs(prob_home - prob_away) < 0.08:
        return None

    # ❌ trop de draw
    if prob_draw > 0.30:
        return None

    # ❌ faux favori
    if prob_home > 0.60 and edge_home < 0.03:
        return None

    # ❌ incohérence marché
    if abs(prob_home - implied_home) > 0.25:
        return None

    # 🔥 score confiance
    confidence = (
        (abs(prob_home - prob_away) * 2)
        + (max(edge_home, edge_away) * 2)
        + (1 - prob_draw)
    )

    confidence = min(max(confidence, 0), 0.85)

    return {
        "prob_home": round(prob_home, 3),
        "prob_draw": round(prob_draw, 3),
        "prob_away": round(prob_away, 3),
        "prob_over": round(prob_over, 3),
        "prob_btts": round(prob_btts, 3),
        "edge_home": round(edge_home, 3),
        "edge_draw": round(edge_draw, 3),
        "edge_away": round(edge_away, 3),
        "confidence": round(confidence, 3)
    }