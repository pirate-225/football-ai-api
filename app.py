from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# SAFE CSV
try:
    teams = pd.read_csv("data_processed/team_stats.csv")
except:
    teams = pd.DataFrame()


@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        try:
            home = request.form.get("home_team")
            away = request.form.get("away_team")

            result = {
                "home": home,
                "away": away,
                "msg": "Test OK"
            }

        except Exception as e:
            print("ERROR:", e)

    return render_template("index.html", teams=teams, result=result, top_bets=[])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)