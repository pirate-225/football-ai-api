from flask import Flask, render_template, request
import pandas as pd
import os

from predict_match import predict_match
from top_bets import get_top_bets

app = Flask(__name__)

# 🔥 SAFE CSV
try:
    teams = pd.read_csv("data_processed/team_stats.csv")
except:
    print("❌ CSV introuvable")
    teams = pd.DataFrame()


@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    # 🔥 TOP BETS (API)
    try:
        top_bets = get_top_bets()
    except Exception as e:
        print("TOP BETS ERROR:", e)
        top_bets = []

    # 🔥 PREDICTION MANUELLE
    if request.method == "POST":

        try:
            home = request.form.get("home_team")
            away = request.form.get("away_team")

            result = predict_match(home, away, 2, 3, 4)

        except Exception as e:
            print("PRED ERROR:", e)

    return render_template(
        "index.html",
        teams=teams,
        result=result,
        top_bets=top_bets
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 RUNNING ON {port}")
    app.run(host="0.0.0.0", port=port)