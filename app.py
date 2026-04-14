from flask import Flask, render_template, request
import pandas as pd
import os
from predict_match import predict_match
from top_bets import get_top_bets

app = Flask(__name__)

# 🔥 SAFE LOAD CSV
try:
    if os.path.exists("data_processed/team_stats.csv"):
        teams_df = pd.read_csv("data_processed/team_stats.csv")
    else:
        print("❌ CSV introuvable")
        teams_df = pd.DataFrame()
except Exception as e:
    print("CSV ERROR:", e)
    teams_df = pd.DataFrame()


@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    try:
        top_bets = get_top_bets()
    except Exception as e:
        print("TOP BETS ERROR:", e)
        top_bets = []

    if request.method == "POST":

        try:
            home_team = request.form.get("home_team")
            away_team = request.form.get("away_team")

            odds_home = request.form.get("odds_home")
            odds_draw = request.form.get("odds_draw")
            odds_away = request.form.get("odds_away")

            result = predict_match(home_team, away_team, odds_home, odds_draw, odds_away)

        except Exception as e:
            print("PREDICTION ERROR:", e)

    return render_template(
        "index.html",
        teams=teams_df,
        result=result,
        top_bets=top_bets
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)