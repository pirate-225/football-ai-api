import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV

print("Training models...")

data = pd.read_csv("data_processed/features.csv")

X = data.drop(columns=["result", "over25", "btts"])
y_result = data["result"]
y_over = data["over25"]
y_btts = data["btts"]

X_train, X_test, y_train, y_test = train_test_split(X, y_result, test_size=0.2)

# RESULT
base_model = RandomForestClassifier(n_estimators=200, max_depth=8, class_weight="balanced")
model_result = CalibratedClassifierCV(base_model, method="sigmoid")
model_result.fit(X_train, y_train)

# OVER
model_over = RandomForestClassifier(n_estimators=120, max_depth=6)
model_over.fit(X_train, y_over.loc[X_train.index])

# BTTS
model_btts = RandomForestClassifier(n_estimators=120, max_depth=6)
model_btts.fit(X_train, y_btts.loc[X_train.index])

os.makedirs("models", exist_ok=True)

joblib.dump(model_result, "models/model_result.pkl")
joblib.dump(model_over, "models/model_over.pkl")
joblib.dump(model_btts, "models/model_btts.pkl")

print("Models trained and saved")