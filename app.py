from data_api import get_team_xg_stats, get_h2h
from data_api import get_odds, get_match_stats
from flask import Flask, render_template, request
import pandas as pd
import os
import requests  # 🔥 manquant

def get_live_matches():
    try:
        url = "https://v3.football.api-sports.io/fixtures"

        headers = {
            "x-apisports-key": "3b63a56a290a3bd3d4b00c5b232d37d3"
        }

        today = pd.Timestamp.today()
        tomorrow = today + pd.Timedelta(days=1)

        dates = [
            today.strftime("%Y-%m-%d"),
            tomorrow.strftime("%Y-%m-%d")
        ]

        matches = []

        for date in dates:

            params = {"date": date}

            res = requests.get(
                url,
                headers=headers,
                params=params
            ).json()

            for f in res.get("response", []):

                matches.append({
                    "home": f["teams"]["home"]["name"],
                    "away": f["teams"]["away"]["name"],
                    "home_id": f["teams"]["home"]["id"],
                    "away_id": f["teams"]["away"]["id"],
                    "league_id": f["league"]["id"],
                    "season": f["league"]["season"],
                    "fixture_id": f["fixture"]["id"]
                })

        return matches

    except Exception as e:
        print("LIVE MATCH ERROR:", e)
        return []

from predict_match import predict_match
from top_bets import get_top_bets

app = Flask(__name__)

try:
    teams = pd.read_csv("data_processed/team_stats.csv")
except:
    teams = pd.DataFrame()


# 🔒 sécurisation des cotes
def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0


@app.route("/", methods=["GET", "POST"])
def index():
    live_matches = []
    result = None
    message = None

    try:
        live_matches = get_live_matches()
    except:
        live_matches = []

    # 🔥 TOP BETS (désactivé proprement pour éviter bugs)
    try:
        top_bets = []
    except:
        top_bets = []

    # 🔥 ANALYSE MANUELLE
    if request.method == "POST":

        # 🔥 VARIABLES PAR DÉFAUT
        shots_home = 5
        shots_away = 5

        pos_home = 50
        pos_away = 50

        xg_home_stats = {"xg_for": 1.2, "xg_against": 1.2}
        xg_away_stats = {"xg_for": 1.2, "xg_against": 1.2}

        h2h_home = 0
        h2h_away = 0

        try:
            home = request.form.get("home_team")
            away = request.form.get("away_team")

            if not home or not away:
                message = "❌ Veuillez sélectionner deux équipes"
                return render_template(
                    "index.html",
                    teams=teams,
                    result=None,
                    top_bets=top_bets,
                    message=message,
                    live_matches=live_matches
                )

            # 🔥 trouver le match sélectionné
            selected_match = None

            for m in live_matches:
                if home.lower() in m["home"].lower() and away.lower() in m["away"].lower():
                    selected_match = m
                    break

            if not selected_match:
                message = "❌ Match non trouvé"
                return render_template(
                    "index.html",
                    teams=teams,
                    result=None,
                    top_bets=top_bets,
                    message=message,
                    live_matches=live_matches
                )

            if selected_match:
                fixture_id = selected_match["fixture_id"]

                # 🔥 xG API
                xg_home_stats = {"xg_for": 1.2, "xg_against": 1.2}
                xg_away_stats = {"xg_for": 1.2, "xg_against": 1.2}

                h2h_home, h2h_away = 0, 0

                xg_away_stats = get_team_xg_stats(
                    selected_match["away_id"],
                    selected_match["league_id"],
                    selected_match["season"]
                )

                # 🔥 H2H API
                h2h_home, h2h_away = get_h2h(
                    selected_match["home_id"],
                    selected_match["away_id"]
                )

                odds_api = get_odds(fixture_id)
                stats_api = get_match_stats(fixture_id)

            print("STATS API RAW:", stats_api)

            # 🔥 FIX INPUT
            odd_home = safe_float(request.form.get("odd_home"))
            odd_draw = safe_float(request.form.get("odd_draw"))
            odd_away = safe_float(request.form.get("odd_away"))

            # 🔥 ODDS API
            if odds_api:
                odd_home = odds_api.get("home", odd_home)
                odd_draw = odds_api.get("draw", odd_draw)
                odd_away = odds_api.get("away", odd_away)

            # 🔥 STATS API (INDÉPENDANT DES COTES)
            if stats_api:
                shots_home = stats_api.get("home", {}).get("shots", 5)
                shots_away = stats_api.get("away", {}).get("shots", 5)

                pos_home = stats_api.get("home", {}).get("possession", 50)
                pos_away = stats_api.get("away", {}).get("possession", 50)

            print("XG FINAL:", xg_home_stats, xg_away_stats)
            print("SHOTS FINAL:", shots_home, shots_away)
            print("POSSESSION:", pos_home, pos_away)

            result = predict_match(
                home,
                away,
                odd_home,
                odd_draw,
                odd_away,
                xg_home_stats,
                xg_away_stats,
                shots_home,
                shots_away,
                pos_home,
                pos_away,
                h2h_home,
                h2h_away
            )

            if result is not None:
                result["odd_home"] = odd_home
                result["odd_draw"] = odd_draw
                result["odd_away"] = odd_away
            else:
                message = "❌ Équipe introuvable ou erreur"

        except Exception as e:
            print("INPUT ERROR:", e)
            message = "❌ Erreur dans les données entrées"

    return render_template(
        "index.html",
        teams=teams,
        result=result,
        top_bets=top_bets,
        message=message,
        live_matches=live_matches
    )

    try:
        return render_template(
            "index.html",
            teams=teams,
            result=result,
            top_bets=top_bets,
            message=message,
            live_matches=live_matches
        )
    except Exception as e:
        print("RENDER ERROR:", e)
        return "Erreur serveur"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)