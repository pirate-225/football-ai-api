import pandas as pd
import math

# 🔥 chargement safe
try:
    teams = pd.read_csv("data_processed/team_stats.csv")
except:
    print("CSV NOT FOUND")
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

        home = teams[teams["Team"] == home_team]
        away = teams[teams["Team"] == away_team]

        if home.empty or away.empty:
            return None

        home = home.iloc[0]
        away = away.iloc[0]

        # 🔥 FORCE ÉQUIPE
        home_strength = (
            home["PPG"] * 0.7 +
            home["GoalsScoredAvg"] * 0.2 -
            home["GoalsConcededAvg"] * 0.1
        ) + 0.35

        away_strength = (
            away["PPG"] * 0.7 +
            away["GoalsScoredAvg"] * 0.2 -
            away["GoalsConcededAvg"] * 0.1
        )

        total = home_strength + away_strength

        prob_home = home_strength / total
        prob_away = away_strength / total
        prob_draw = max(0.18, 1 - (prob_home + prob_away))

        # 🔥 xG SIMPLE
        home_xg = (home["GoalsScoredAvg"] + away["GoalsConcededAvg"]) / 2
        away_xg = (away["GoalsScoredAvg"] + home["GoalsConcededAvg"]) / 2

        # 🔥 POISSON
        max_goals = 5
        prob_over = 0
        prob_btts = 0

        for i in range(max_goals + 1):
            for j in range(max_goals + 1):

                p = poisson(home_xg, i) * poisson(away_xg, j)

                if i + j >= 3:
                    prob_over += p

                if i > 0 and j > 0:
                    prob_btts += p

        # 🔥 bookmaker
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