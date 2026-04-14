from flask import Flask, render_template, request
import pandas as pd
import os

from predict_match import predict_match

app = Flask(__name__)

try:
    teams = pd.read_csv("data_processed/team_stats.csv")
except:
    teams = pd.DataFrame()


@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        home = request.form.get("home_team")
        away = request.form.get("away_team")

        if home and away:

            result = predict_match(home, away, 2, 3, 4)

    return render_template(
        "index.html",
        teams=teams,
        result=result,
        top_bets=[]
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)