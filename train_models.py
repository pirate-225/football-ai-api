import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV

print("Lecture features...")
data = pd.read_csv("data_processed/features.csv")

features = [
    "home_points_per_game",
    "away_points_per_game",
    "points_diff",
    "goal_diff_diff",
    "position_diff",
    "elo_diff",
    "form_diff"
]

X = data[features]
y_result = data["result"]
y_over = data["over25"]
y_btts = data["btts"]

X_train, X_test, y_train, y_test = train_test_split(X, y_result, test_size=0.2, random_state=42)

model_result = RandomForestClassifier(n_estimators=300)
model_result = CalibratedClassifierCV(model_result, method='sigmoid')
model_result.fit(X_train, y_train)

model_over = RandomForestClassifier(n_estimators=200)
model_over = CalibratedClassifierCV(model_over, method='sigmoid')
model_over.fit(X_train, y_over.loc[X_train.index])

model_btts = RandomForestClassifier(n_estimators=200)
model_btts = CalibratedClassifierCV(model_btts, method='sigmoid')
model_btts.fit(X_train, y_btts.loc[X_train.index])

joblib.dump(model_result, "models/model_result.pkl")
joblib.dump(model_over, "models/model_over.pkl")
joblib.dump(model_btts, "models/model_btts.pkl")

print("Modèles sauvegardés")