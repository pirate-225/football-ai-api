from flask import Flask, render_template, request
from predict_match import predict_match

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        home_team = request.form["home_team"]
        away_team = request.form["away_team"]
        odds_home = request.form["odds_home"]
        odds_draw = request.form["odds_draw"]
        odds_away = request.form["odds_away"]

        result = predict_match(home_team, away_team, odds_home, odds_draw, odds_away)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run()