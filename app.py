from flask import Flask, render_template, request
import pickle
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_result = pickle.load(open(os.path.join(BASE_DIR, "model_result.pkl"), "rb"))
model_over = pickle.load(open(os.path.join(BASE_DIR, "model_over.pkl"), "rb"))
model_btts = pickle.load(open(os.path.join(BASE_DIR, "model_btts.pkl"), "rb"))

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        B365H = float(request.form["B365H"])
        B365D = float(request.form["B365D"])
        B365A = float(request.form["B365A"])
        HS = float(request.form["HS"])
        AS = float(request.form["AS"])
        HST = float(request.form["HST"])
        AST = float(request.form["AST"])
        HC = float(request.form["HC"])
        AC = float(request.form["AC"])

        match = pd.DataFrame([{
            "B365H":B365H,
            "B365D":B365D,
            "B365A":B365A,
            "HS":HS,
            "AS":AS,
            "HST":HST,
            "AST":AST,
            "HC":HC,
            "AC":AC
        }])

        res = model_result.predict_proba(match)
        over = model_over.predict_proba(match)
        btts = model_btts.predict_proba(match)

        result = {
            "home": round(res[0][2]*100,1),
            "draw": round(res[0][1]*100,1),
            "away": round(res[0][0]*100,1),
            "over": round(over[0][1]*100,1),
            "btts": round(btts[0][1]*100,1)
        }

        decision = "Match à éviter"

        if result["home"] > 60:
            decision = "Victoire domicile"
        elif result["away"] > 60:
            decision = "Victoire extérieur"
        elif result["over"] > 60:
            decision = "Over 2.5"
        elif result["btts"] > 60:
            decision = "BTTS"
        elif result["home"] > 45 and result["draw"] > 25:
            decision = "1X"
        elif result["away"] > 45 and result["draw"] > 25:
            decision = "X2"

        return render_template("index.html", result=result, decision=decision)

    return render_template("index.html")

if __name__ == "__main__":
    app.run()