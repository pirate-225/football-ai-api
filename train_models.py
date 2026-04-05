import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# Charger dataset
df = pd.read_csv("data_processed/features.csv")

df = df.dropna()

# Séparer Train / Test (80% ancien / 20% récent)
split_index = int(len(df) * 0.8)

train = df.iloc[:split_index]
test = df.iloc[split_index:]

# FEATURES
features = [
    'home_points_per_game',
    'home_goals_scored_avg',
    'home_goals_conceded_avg',
    'home_goal_diff_avg',
    'home_over_ratio',
    'home_btts_ratio',
    'home_form',

    'away_points_per_game',
    'away_goals_scored_avg',
    'away_goals_conceded_avg',
    'away_goal_diff_avg',
    'away_over_ratio',
    'away_btts_ratio',
    'away_form',

    'form_diff',
    'points_diff',
    'goal_diff_diff',
    'over_diff',
    'btts_diff',
    'odds_ratio',
    
    'home_elo',
    'away_elo',
    'elo_diff',
    
    'odds_home',
    'odds_draw',
    'odds_away'
]

X_train = train[features]
X_test = test[features]

y_train_r = train['result']
y_test_r = test['result']

y_train_o = train['over25']
y_test_o = test['over25']

y_train_b = train['btts']
y_test_b = test['btts']

# MODEL RESULT
model_result = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42
)
model_result.fit(X_train, y_train_r)

pred_r = model_result.predict(X_test)
print("Accuracy RESULT :", accuracy_score(y_test_r, pred_r))

# MODEL OVER
model_over = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42
)
model_over.fit(X_train, y_train_o)

pred_o = model_over.predict(X_test)
print("Accuracy OVER 2.5 :", accuracy_score(y_test_o, pred_o))

# MODEL BTTS
model_btts = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42
)
model_btts.fit(X_train, y_train_b)

pred_b = model_btts.predict(X_test)
print("Accuracy BTTS :", accuracy_score(y_test_b, pred_b))

# Save models
os.makedirs("models", exist_ok=True)

joblib.dump(model_result, "models/model_result.pkl")
joblib.dump(model_over, "models/model_over.pkl")
joblib.dump(model_btts, "models/model_btts.pkl")

print("Modèles sauvegardés")