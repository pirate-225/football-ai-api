import pandas as pd
import joblib
import numpy as np

# Charger modèles
model_result = joblib.load("models/model_result.pkl")
model_over = joblib.load("models/model_over.pkl")
model_btts = joblib.load("models/model_btts.pkl")

# Charger stats équipes
team_stats = pd.read_csv("data_processed/team_stats.csv")

# -----------------------
# INPUT MATCH
# -----------------------
home_team = "Lyon"
away_team = "Lille"

odds_home = 2.10
odds_draw = 3.40
odds_away = 3.30

# -----------------------
# Récupérer stats équipes
# -----------------------
home_stats = team_stats[team_stats['team'] == home_team].iloc[0]
away_stats = team_stats[team_stats['team'] == away_team].iloc[0]

home_features = [
    home_stats['points_per_game'],
    home_stats['goals_scored_avg'],
    home_stats['goals_conceded_avg'],
    home_stats['goal_diff'],
    home_stats['over_ratio'],
    home_stats['btts_ratio'],
    home_stats['form']
]

away_features = [
    away_stats['points_per_game'],
    away_stats['goals_scored_avg'],
    away_stats['goals_conceded_avg'],
    away_stats['goal_diff'],
    away_stats['over_ratio'],
    away_stats['btts_ratio'],
    away_stats['form']
]

# Diff features
form_diff = home_features[6] - away_features[6]
points_diff = home_features[0] - away_features[0]
goal_diff_diff = home_features[3] - away_features[3]
over_diff = home_features[4] - away_features[4]
btts_diff = home_features[5] - away_features[5]

odds_ratio = odds_home / odds_away if odds_away != 0 else 0

# ELO
home_elo = home_stats['elo']
away_elo = away_stats['elo']
elo_diff = home_elo - away_elo

features = [
    *home_features,
    *away_features,
    form_diff,
    points_diff,
    goal_diff_diff,
    over_diff,
    btts_diff,
    odds_ratio,
    home_elo,
    away_elo,
    elo_diff,
    odds_home,
    odds_draw,
    odds_away
]

X = np.array(features).reshape(1, -1)

# -----------------------
# PREDICTIONS
# -----------------------
proba_result = model_result.predict_proba(X)[0]
proba_over = model_over.predict_proba(X)[0][1]
proba_btts = model_btts.predict_proba(X)[0][1]

home_prob = proba_result[2]
draw_prob = proba_result[1]
away_prob = proba_result[0]

print("\n===== PREDICTIONS =====")
print(home_team, "vs", away_team)
print("Home win:", round(home_prob, 3))
print("Draw:", round(draw_prob, 3))
print("Away win:", round(away_prob, 3))
print("Over 2.5:", round(proba_over, 3))
print("BTTS:", round(proba_btts, 3))

# -----------------------
# VALUE BET
# -----------------------
book_home = 1 / odds_home
book_draw = 1 / odds_draw
book_away = 1 / odds_away

total = book_home + book_draw + book_away
book_home /= total
book_draw /= total
book_away /= total

edge_home = home_prob - book_home
edge_draw = draw_prob - book_draw
edge_away = away_prob - book_away

print("\n===== VALUE BET =====")
print("Edge Home:", round(edge_home,3))
print("Edge Draw:", round(edge_draw,3))
print("Edge Away:", round(edge_away,3))

# Pick final
print("\n===== PICK =====")
if home_prob > draw_prob and home_prob > away_prob:
    print("Prediction: HOME WIN")
elif away_prob > home_prob and away_prob > draw_prob:
    print("Prediction: AWAY WIN")
else:
    print("Prediction: DRAW")

# Confidence
max_prob = max(home_prob, draw_prob, away_prob)

if max_prob > 0.60:
    print("Confidence: HIGH")
elif max_prob > 0.52:
    print("Confidence: MEDIUM")
else:
    print("Confidence: LOW")