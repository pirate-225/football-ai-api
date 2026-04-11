from flask import Flask, render_template, request
import pandas as pd
import os
from predict_match import predict_match
from top_bets import get_top_bets

app = Flask(__name__)

teams_df = pd.read_csv("data_processed/team_stats.csv")

@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    try:
        top_bets = get_top_bets()
    except:
        top_bets = []

    if request.method == "POST":
        home_team = request.form["home_team"]
        away_team = request.form["away_team"]

        odds_home = request.form["odds_home"]
        odds_draw = request.form["odds_draw"]
        odds_away = request.form["odds_away"]

        result = predict_match(home_team, away_team, odds_home, odds_draw, odds_away)

    return render_template(
        "index.html",
        teams=teams_df,
        result=result,
        top_bets=top_bets
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 APP RUNNING on port {port}")
    app.run(host="0.0.0.0", port=port)