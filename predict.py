import joblib
import numpy as np

# Charger modèles
model_result = joblib.load("models/model_result.pkl")
model_over = joblib.load("models/model_over.pkl")
model_btts = joblib.load("models/model_btts.pkl")

# -----------------------
# INPUT MATCH FEATURES
# -----------------------
# Exemple de match (à remplacer par ton site Flask plus tard)

features = [
    1.5, 1.4, 1.1, 0.3, 0.55, 0.50, 0.60,   # home stats
    1.2, 1.1, 1.3, -0.2, 0.45, 0.52, 0.40,  # away stats
    0.20, 0.30, 0.50, 0.10, -0.05, 1.2,     # diff stats
    1550, 1500, 50,                        # elo
    1.90, 3.40, 4.20                       # odds
]

X = np.array(features).reshape(1, -1)

# -----------------------
# PREDICTIONS
# -----------------------
proba_result = model_result.predict_proba(X)[0]
proba_over = model_over.predict_proba(X)[0][1]
proba_btts = model_btts.predict_proba(X)[0][1]

print("------ PREDICTIONS ------")
print("Home win probability:", round(proba_result[2], 3))
print("Draw probability:", round(proba_result[1], 3))
print("Away win probability:", round(proba_result[0], 3))

print("Over 2.5 probability:", round(proba_over, 3))
print("BTTS probability:", round(proba_btts, 3))

# -----------------------
# BOOKMAKER PROBABILITIES
# -----------------------
odds_home = features[-3]
odds_draw = features[-2]
odds_away = features[-1]

book_home = 1 / odds_home
book_draw = 1 / odds_draw
book_away = 1 / odds_away

# Normalize bookmaker probs
total = book_home + book_draw + book_away
book_home /= total
book_draw /= total
book_away /= total

# -----------------------
# EDGE / VALUE BET
# -----------------------
edge_home = proba_result[2] - book_home
edge_draw = proba_result[1] - book_draw
edge_away = proba_result[0] - book_away

print("\n------ VALUE BET ------")

if edge_home > 0.05:
    print("Value bet HOME")
if edge_draw > 0.05:
    print("Value bet DRAW")
if edge_away > 0.05:
    print("Value bet AWAY")

print("Edge Home:", round(edge_home,3))
print("Edge Draw:", round(edge_draw,3))
print("Edge Away:", round(edge_away,3))

# Over / BTTS value
book_over = 0.5
book_btts = 0.5

edge_over = proba_over - book_over
edge_btts = proba_btts - book_btts

print("\n------ OVER / BTTS VALUE ------")
print("Edge Over:", round(edge_over,3))
print("Edge BTTS:", round(edge_btts,3))