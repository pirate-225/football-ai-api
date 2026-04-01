import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Charger dataset
data = pd.read_csv("dataset.csv")

features = [
    "B365H","B365D","B365A",
    "HS","AS","HST","AST","HC","AC"
]

X = data[features]

# Targets
y_result = data["Result"]
y_over = data["Over25"]
y_btts = data["BTTS"]

# Split
X_train, X_test, y_train_res, y_test_res = train_test_split(X, y_result, test_size=0.2)
X_train, X_test, y_train_over, y_test_over = train_test_split(X, y_over, test_size=0.2)
X_train, X_test, y_train_btts, y_test_btts = train_test_split(X, y_btts, test_size=0.2)

# Modèles
model_result = RandomForestClassifier(n_estimators=100)
model_over = RandomForestClassifier(n_estimators=100)
model_btts = RandomForestClassifier(n_estimators=100)

model_result.fit(X_train, y_train_res)
model_over.fit(X_train, y_train_over)
model_btts.fit(X_train, y_train_btts)

# Sauvegarde
pickle.dump(model_result, open("model_result.pkl","wb"))
pickle.dump(model_over, open("model_over.pkl","wb"))
pickle.dump(model_btts, open("model_btts.pkl","wb"))

print("Modèles IA entraînés")