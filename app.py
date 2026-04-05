from flask import Flask, render_template, request
import pandas as pd
from predict_match import predict_match

app = Flask(__name__)

team_stats = pd.read_csv("data_processed/team_stats.csv")
teams = sorted(team_stats["Team"].unique())

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        home_team = request.form["home_team"]
        away_team = request.form["away_team"]
        odds_home = request.form["odds_home"]
        odds_draw = request.form["odds_draw"]
        odds_away = request.form["odds_away"]

        prediction = predict_match(home_team, away_team, odds_home, odds_draw, odds_away)

    return render_template("index.html", teams=teams, prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)