from flask import Flask, render_template, request
import pandas as pd
from predict_match import predict_match
from api.get_today_matches import get_today_matches

app = Flask(__name__)

teams_df = pd.read_csv("data_processed/team_stats.csv")

@app.route("/", methods=["GET", "POST"])
def index():

    print("🔥 ROUTE INDEX APPELÉE")

    result = None

    print("📡 Appel API matchs du jour...")
    today_matches = get_today_matches()

    print("📊 Matchs récupérés :", len(today_matches))

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

if __name__ == "__main__":
    app.run(debug=True)