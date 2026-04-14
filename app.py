from flask import Flask, render_template, request
import pandas as pd
import os

from predict_match import predict_match
from top_bets import get_top_bets

app = Flask(__name__)

# 🔥 SAFE LOAD CSV
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
    except:
        top_bets = []

    if request.method == "POST":

        home = request.form.get("home_team")
        away = request.form.get("away_team")

        if home and away:

            # 🔥 cotes fixes (safe)
            odd_home = 2.0
            odd_draw = 3.2
            odd_away = 3.5

            result = predict_match(home, away, odd_home, odd_draw, odd_away)

            if result:
                result["odd_home"] = odd_home
                result["odd_draw"] = odd_draw
                result["odd_away"] = odd_away

    return render_template(
        "index.html",
        teams=teams,
        result=result,
        top_bets=top_bets
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)