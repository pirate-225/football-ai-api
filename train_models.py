import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

print("Lecture features...")

data = pd.read_csv("data_processed/features.csv")

# Targets
y_result = data["Result"]
y_over = data["Over25"]
y_btts = data["BTTS"]

# Features
X = data.drop(["Result", "Over25", "BTTS"], axis=1)

# Split
X_train, X_test, y_train_result, y_test_result = train_test_split(X, y_result, test_size=0.2)
_, _, y_train_over, y_test_over = train_test_split(X, y_over, test_size=0.2)
_, _, y_train_btts, y_test_btts = train_test_split(X, y_btts, test_size=0.2)

# Models
model_result = RandomForestClassifier(n_estimators=100)
model_over = RandomForestClassifier(n_estimators=100)
model_btts = RandomForestClassifier(n_estimators=100)

# Train
model_result.fit(X_train, y_train_result)
model_over.fit(X_train, y_train_over)
model_btts.fit(X_train, y_train_btts)

# Accuracy
print("Accuracy RESULT :", model_result.score(X_test, y_test_result))
print("Accuracy OVER 2.5 :", model_over.score(X_test, y_test_over))
print("Accuracy BTTS :", model_btts.score(X_test, y_test_btts))

# Save models
joblib.dump(model_result, "models/model_result.pkl")
joblib.dump(model_over, "models/model_over.pkl")
joblib.dump(model_btts, "models/model_btts.pkl")

print("Modèles sauvegardés")