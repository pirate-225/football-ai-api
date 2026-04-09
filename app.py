from flask import Flask, render_template, request
import pandas as pd
import os
from predict_match import predict_match
from api.get_today_matches import get_today_matches

app = Flask(__name__)

teams_df = pd.read_csv("data_processed/team_stats.csv")

@app.route("/", methods=["GET", "POST"])
def index():

    print("🔥 APP RUNNING")

    result = None
    today_matches = get_today_matches()

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
        today_matches=today_matches
    )

# 🔥 FIX RENDER PORT (OBLIGATOIRE)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)