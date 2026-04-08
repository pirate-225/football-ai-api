from flask import Flask, render_template, request
import pandas as pd
from predict_match import predict_match

app = Flask(__name__)

teams_df = pd.read_csv("data_processed/team_stats.csv")

def get_leagues():
    if "league_name" in teams_df.columns:
        return sorted(teams_df["league_name"].unique())
    return ["All"]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    league = request.form.get("league") if request.method == "POST" else None

    if league and league != "All":
        teams = teams_df[teams_df["league_name"] == league]
    else:
        teams = teams_df

    teams_list = teams.sort_values("PointsPerGame", ascending=False)

    if request.method == "POST":
        home_team = request.form["home_team"]
        away_team = request.form["away_team"]

        odds_home = request.form["odds_home"]
        odds_draw = request.form["odds_draw"]
        odds_away = request.form["odds_away"]

        result = predict_match(home_team, away_team, odds_home, odds_draw, odds_away)

    return render_template(
        "index.html",
        teams=teams_list,
        leagues=get_leagues(),
        selected_league=league,
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)