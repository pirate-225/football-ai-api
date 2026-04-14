from flask import Flask, render_template, request
import pandas as pd
import os

from predict_match import predict_match
from top_bets import get_top_bets

app = Flask(__name__)

# 🔥 LOAD CSV SAFE
try:
    teams = pd.read_csv("data_processed/team_stats.csv")
except:
    teams = pd.DataFrame()


@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    # 🔥 TOP BETS
    try:
        top_bets = get_top_bets()
    except Exception as e:
        print("TOP BETS ERROR:", e)
        top_bets = []

    # 🔥 FORM SUBMIT
    if request.method == "POST":

        try:
            home = request.form.get("home_team")
            away = request.form.get("away_team")

            # 🔥 sécurité
            if not home or not away:
                return render_template(
                    "index.html",
                    teams=teams,
                    result=None,
                    top_bets=top_bets
                )

            # 🔥 cotes visibles même en manuel
odd_home = 2.0
odd_draw = 3.2
odd_away = 3.5

result = predict_match(home, away, odd_home, odd_draw, odd_away)

# 🔥 on ajoute les cotes au résultat
if result:
    result["odd_home"] = odd_home
    result["odd_draw"] = odd_draw
    result["odd_away"] = odd_away

        except Exception as e:
            print("PRED ERROR:", e)
            result = None

    return render_template(
        "index.html",
        teams=teams,
        result=result,
        top_bets=top_bets
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)