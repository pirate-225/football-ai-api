import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# 🔥 récupération données
home_attack = home["HomeAttack"]
away_attack = away["AwayAttack"]

home_def = home["GoalsConcededAvg"]
away_def = away["GoalsConcededAvg"]

home_form = home["Form"]
away_form = away["Form"]

home_elo = home["ELO"]
away_elo = away["ELO"]


# 🔥 force brute
home_strength = (home_attack / away_def)
away_strength = (away_attack / home_def)


# 🔥 impact forme
form_diff = (home_form - away_form) / 3
home_strength *= (1 + form_diff)
away_strength *= (1 - form_diff)


# 🔥 impact elo (très important)
elo_diff = (home_elo - away_elo) / 400

home_strength *= (1 + elo_diff)
away_strength *= (1 - elo_diff)


# 🔥 normalisation (CLÉ)
total = home_strength + away_strength

prob_home = home_strength / total
prob_away = away_strength / total

# 🔥 draw réaliste
prob_draw = 1 - abs(prob_home - prob_away)
prob_draw *= 0.25

# 🔥 renormalisation
total = prob_home + prob_draw + prob_away

prob_home /= total
prob_draw /= total
prob_away /= total


# 🔥 OVER (corrigé)
goal_expectation = (home_attack + away_attack) / 2

prob_over = sigmoid(goal_expectation - 2.4)


# 🔥 BTTS (corrigé)
prob_btts = sigmoid((home_attack * away_attack) - 1.2)


# 🔥 EDGE (réel)
implied_home = 1 / odd_home
implied_draw = 1 / odd_draw
implied_away = 1 / odd_away

edge_home = prob_home - implied_home
edge_draw = prob_draw - implied_draw
edge_away = prob_away - implied_away