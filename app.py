from flask import Flask, render_template, request
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

# Charger modèles
model_result = joblib.load("models/model_result.pkl")
model_over = joblib.load("models/model_over.pkl")
model_btts = joblib.load("models/model_btts.pkl")

# Charger stats équipes
team_stats = pd.read_csv("data_processed/team_stats.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        home_team = request.form["home_team"]
        away_team = request.form["away_team"]
        odds_home = float(request.form["odds_home"])
        odds_draw = float(request.form["odds_draw"])
        odds_away = float(request.form["odds_away"])

        home_stats = team_stats[team_stats['team'] == home_team].iloc[0]
        away_stats = team_stats[team_stats['team'] == away_team].iloc[0]

        home_features = [
            home_stats['points_per_game'],
            home_stats['goals_scored_avg'],
            home_stats['goals_conceded_avg'],
            home_stats['goal_diff'],
            home_stats['over_ratio'],
            home_stats['btts_ratio'],
            home_stats['form']
        ]

        away_features = [
            away_stats['points_per_game'],
            away_stats['goals_scored_avg'],
            away_stats['goals_conceded_avg'],
            away_stats['goal_diff'],
            away_stats['over_ratio'],
            away_stats['btts_ratio'],
            away_stats['form']
        ]

        form_diff = home_features[6] - away_features[6]
        points_diff = home_features[0] - away_features[0]
        goal_diff_diff = home_features[3] - away_features[3]
        over_diff = home_features[4] - away_features[4]
        btts_diff = home_features[5] - away_features[5]
        odds_ratio = odds_home / odds_away if odds_away != 0 else 0

        home_elo = home_stats['elo']
        away_elo = away_stats['elo']
        elo_diff = home_elo - away_elo

        features = [
            *home_features,
            *away_features,
            form_diff,
            points_diff,
            goal_diff_diff,
            over_diff,
            btts_diff,
            odds_ratio,
            home_elo,
            away_elo,
            elo_diff,
            odds_home,
            odds_draw,
            odds_away
        ]

        X = np.array(features).reshape(1, -1)

        proba_result = model_result.predict_proba(X)[0]
        proba_over = model_over.predict_proba(X)[0][1]
        proba_btts = model_btts.predict_proba(X)[0][1]

        prediction = {
            "home": round(proba_result[2], 3),
            "draw": round(proba_result[1], 3),
            "away": round(proba_result[0], 3),
            "over": round(proba_over, 3),
            "btts": round(proba_btts, 3),
        }

    teams = sorted(team_stats['team'].unique())

    return render_template("index.html", prediction=prediction, teams=teams)

if __name__ == "__main__":
    app.run(debug=True)