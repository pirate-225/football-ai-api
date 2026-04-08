import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV

print("Training models...")

data = pd.read_csv("data_processed/features.csv")

features = [
    "home_ppg",
    "away_ppg",
    "ppg_diff",
    "form_diff",
    "attack_diff",
    "defense_diff",
    "strength_diff",
    "exp_diff"
]

X = data[features]

y_result = data["result"]
y_over = data["over25"]
y_btts = data["btts"]

X_train, X_test, y_train, y_test = train_test_split(X, y_result, test_size=0.2)

# 🔥 modèle calibré (IMPORTANT)
base_model = RandomForestClassifier(
    n_estimators=150,
    max_depth=7,
    random_state=42,
    class_weight="balanced"
)

model_result = CalibratedClassifierCV(base_model, method='sigmoid')
model_result.fit(X_train, y_train)

model_over = RandomForestClassifier(n_estimators=100, max_depth=5)
model_over.fit(X_train, y_over.loc[X_train.index])

model_btts = RandomForestClassifier(n_estimators=100, max_depth=5)
model_btts.fit(X_train, y_btts.loc[X_train.index])

os.makedirs("models", exist_ok=True)

joblib.dump(model_result, "models/model_result.pkl", compress=9)
joblib.dump(model_over, "models/model_over.pkl", compress=9)
joblib.dump(model_btts, "models/model_btts.pkl", compress=9)

print("Models trained and saved")