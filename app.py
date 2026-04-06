from flask import Flask, render_template, request
import pandas as pd
import os
from predict_match import predict_match

app = Flask(__name__)

def get_teams():
    if os.path.exists("data_processed/team_stats.csv"):
        df = pd.read_csv("data_processed/team_stats.csv")
        return sorted(df["Team"].unique())
    return []

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    teams = get_teams()

    if request.method == "POST":
        home_team = request.form["home_team"]
        away_team = request.form["away_team"]
        odds_home = request.form["odds_home"]
        odds_draw = request.form["odds_draw"]
        odds_away = request.form["odds_away"]

        result = predict_match(home_team, away_team, odds_home, odds_draw, odds_away)

    return render_template("index.html", teams=teams, result=result)

if __name__ == "__main__":
    app.run()