import pickle
import pandas as pd

# Charger modèles
model_result = pickle.load(open("model_result.pkl","rb"))
model_over = pickle.load(open("model_over.pkl","rb"))
model_btts = pickle.load(open("model_btts.pkl","rb"))

# Données match
match = pd.DataFrame([{
    "B365H": 1.80,
    "B365D": 3.50,
    "B365A": 4.50,
    "HS": 12,
    "AS": 9,
    "HST": 5,
    "AST": 3,
    "HC": 6,
    "AC": 4
}])

# Probabilités
res = model_result.predict_proba(match)
over = model_over.predict_proba(match)
btts = model_btts.predict_proba(match)

home = res[0][2]
draw = res[0][1]
away = res[0][0]
over25 = over[0][1]
btts_yes = btts[0][1]

print("\n----- ANALYSE IA -----")

print("\n1X2 :")
print("Home:", round(home*100,1), "%")
print("Draw:", round(draw*100,1), "%")
print("Away:", round(away*100,1), "%")

print("\nOver 2.5:", round(over25*100,1), "%")
print("BTTS:", round(btts_yes*100,1), "%")

# Décision automatique
print("\n----- DECISION IA -----")

if home > 0.6:
    print("Pari conseillé : Victoire domicile")
elif away > 0.6:
    print("Pari conseillé : Victoire extérieur")
elif over25 > 0.6:
    print("Pari conseillé : Over 2.5")
elif btts_yes > 0.6:
    print("Pari conseillé : BTTS")
elif home > 0.45 and draw > 0.25:
    print("Pari conseillé : 1X")
elif away > 0.45 and draw > 0.25:
    print("Pari conseillé : X2")
else:
    print("Match à éviter")