from flask import Flask, render_template, request
import pickle
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_model(name):
    path = os.path.join(BASE_DIR, name)
    if os.path.exists(path):
        return pickle.load(open(path, "rb"))
    else:
        return None

model_result = load_model("model_result.pkl")
model_over = load_model("model_over.pkl")
model_btts = load_model("model_btts.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            B365H = float(request.form.get("B365H", 0))
            B365D = float(request.form.get("B365D", 0))
            B365A = float(request.form.get("B365A", 0))
            HS = float(request.form.get("HS", 0))
            AS = float(request.form.get("AS", 0))
            HST = float(request.form.get("HST", 0))
            AST = float(request.form.get("AST", 0))
            HC = float(request.form.get("HC", 0))
            AC = float(request.form.get("AC", 0))

            match = pd.DataFrame([{
                "B365H": B365H,
                "B365D": B365D,
                "B365A": B365A,
                "HS": HS,
                "AS": AS,
                "HST": HST,
                "AST": AST,
                "HC": HC,
                "AC": AC
            }])

            result = {}
            decision = "Pas de modèle chargé"

            if model_result:
                res = model_result.predict_proba(match)
                result["home"] = round(res[0][2]*100, 1)
                result["draw"] = round(res[0][1]*100, 1)
                result["away"] = round(res[0][0]*100, 1)

            if model_over:
                over = model_over.predict_proba(match)
                result["over"] = round(over[0][1]*100, 1)

            if model_btts:
                btts = model_btts.predict_proba(match)
                result["btts"] = round(btts[0][1]*100, 1)

            if "home" in result and result["home"] > 60:
                decision = "Victoire domicile"
            elif "away" in result and result["away"] > 60:
                decision = "Victoire extérieur"
            elif "over" in result and result["over"] > 60:
                decision = "Over 2.5"
            elif "btts" in result and result["btts"] > 60:
                decision = "BTTS"

            return render_template("index.html", result=result, decision=decision)

        except Exception as e:
            return str(e)

    return render_template("index.html")

if __name__ == "__main__":
    app.run()