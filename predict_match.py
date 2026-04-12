import pandas as pd
import math

teams = pd.read_csv("data_processed/team_stats.csv")


def poisson_prob(lmbda, k):
    return (lmbda ** k * math.exp(-lmbda)) / math.factorial(k)


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    home_df = teams[teams["Team"] == home_team]
    away_df = teams[teams["Team"] == away_team]

    if home_df.empty or away_df.empty:
        return None

    home = home_df.iloc[0]
    away = away_df.iloc[0]

    # 🔥 FORCE TYPE ELO (CRUCIAL)
    home_rating = home["PPG"] * 50
    away_rating = away["PPG"] * 50

    # 🔥 DIFFÉRENCE DE NIVEAU
    rating_diff = home_rating - away_rating

    # 🔥 AVANTAGE DOMICILE
    rating_diff += 10

    # 🔥 conversion en probabilité logistique
    prob_home = 1 / (1 + 10 ** (-rating_diff / 40))
    prob_away = 1 - prob_home

    # 🔥 draw réaliste
    prob_draw = 0.25 * (1 - abs(prob_home - prob_away))

    # 🔥 normalisation
    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    # 🔥 goals pour over/btts
    home_xg = (home["GoalsScoredAvg"] + away["GoalsConcededAvg"]) / 2 + 0.2
    away_xg = (away["GoalsScoredAvg"] + home["GoalsConcededAvg"]) / 2

    prob_over = min(0.85, (home_xg + away_xg) / 2.8)
    prob_btts = min(0.85, (home_xg * away_xg) / 2.5)

    # 🔥 bookmaker corrigé
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

    confidence = max(prob_home, prob_draw, prob_away)

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