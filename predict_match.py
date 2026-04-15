import pandas as pd
import math

# 🔥 LOAD DATA
try:
    teams = pd.read_csv("data_processed/team_stats.csv")
except:
    teams = pd.DataFrame()


def poisson(lmbda, k):
    try:
        return (lmbda ** k * math.exp(-lmbda)) / math.factorial(k)
    except:
        return 0


def predict_match(home_team, away_team, odd_home, odd_draw, odd_away):

    try:

        if teams.empty:
            return None

        home_df = teams[teams["Team"] == home_team]
        away_df = teams[teams["Team"] == away_team]

        if home_df.empty or away_df.empty:
            return None

        home = home_df.iloc[0]
        away = away_df.iloc[0]

        # 🔥 STATS DE BASE
        home_attack = float(home["GoalsScoredAvg"])
        home_defense = float(home["GoalsConcededAvg"])

        away_attack = float(away["GoalsScoredAvg"])
        away_defense = float(away["GoalsConcededAvg"])

        # 🔥 ELO IMPACT (TRÈS IMPORTANT)
        home_elo = float(home.get("ELO", 1000))
        away_elo = float(away.get("ELO", 1000))

        elo_diff = (home_elo - away_elo) / 400

        home_attack *= (1 + elo_diff * 0.1)
        away_attack *= (1 - elo_diff * 0.1)

        # 🔥 FORME (pondérée correctement)
        home_form = float(home.get("PPG", 1.5))
        away_form = float(away.get("PPG", 1.5))

        home_attack = home_attack * (1 + (home_form - 1.5) * 0.15)
        away_attack = away_attack * (1 + (away_form - 1.5) * 0.15)

        # 🔥 sécurité
        home_attack = max(0.5, home_attack)
        away_attack = max(0.5, away_attack)

        # 🔥 avantage domicile
        home_adv = 1.1

        home_strength = (home_attack * away_defense) * home_adv
        away_strength = (away_attack * home_defense)

        total = home_strength + away_strength

        prob_home = home_strength / total
        prob_away = away_strength / total

        # 🔥 draw réaliste
        prob_draw = 1 - (prob_home + prob_away)
        prob_draw = max(0.20, min(prob_draw, 0.30))

        # 🔥 xG
        home_xg = home_attack * away_defense
        away_xg = away_attack * home_defense

        # 🔥 POISSON
        prob_over = 0
        prob_btts = 0

        for i in range(6):
            for j in range(6):

                p = poisson(home_xg, i) * poisson(away_xg, j)

                if i + j >= 3:
                    prob_over += p

                if i > 0 and j > 0:
                    prob_btts += p

        # 🔥 BOOKMAKER
        imp_home = 1 / odd_home
        imp_draw = 1 / odd_draw
        imp_away = 1 / odd_away

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

    except Exception as e:
        print("MODEL ERROR:", e)
        return None