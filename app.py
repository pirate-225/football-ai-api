from flask import Flask, render_template, request
import pandas as pd
import os
import requests

def get_live_matches():
    try:
        url = "https://v3.football.api-sports.io/fixtures"

        headers = {
            "x-apisports-key": "3b63a56a290a3bd3d4b00c5b232d37d3"
        }

        params = {
            "date": pd.Timestamp.today().strftime("%Y-%m-%d"),
            "league": "39,61,78,140,135,2,3,848"  
        }

        res = requests.get(url, headers=headers, params=params).json()

        matches = []

        for f in res.get("response", [])[:20]:
            matches.append({
                "home": f["teams"]["home"]["name"],
                "away": f["teams"]["away"]["name"],
                "league": f["league"]["name"]
            })

        return matches

    except Exception as e:
        print("API ERROR:", e)
        return []

from predict_match import predict_match
from top_bets import get_top_bets

app = Flask(__name__)

try:
    teams = pd.read_csv("data_processed/team_stats.csv")
except:
    teams = pd.DataFrame()


@app.route("/", methods=["GET", "POST"])
def index():

    return "OK"

    try:
        top_bets = get_top_bets()
    except Exception as e:
        print("TOP BETS ERROR:", e)
        top_bets = []

    try:
        live_matches = get_live_matches()
    except:
        live_matches = []

    print("LIVE MATCHES:", live_matches)

    # 🔥 TOP BETS API
    try:
        top_bets = get_top_bets()
        live_matches = get_live_matches()
    except:
        top_bets = []

    # 🔥 ANALYSE MANUELLE
    if request.method == "POST":

        try:
            home = request.form.get("home_team")
            away = request.form.get("away_team")

            odd_home = float(request.form.get("odd_home"))
            odd_draw = float(request.form.get("odd_draw"))
            odd_away = float(request.form.get("odd_away"))

            try:
                result = predict_match(home, away, odd_home, odd_draw, odd_away)
            except Exception as e:
                print("ERROR PREDICT:", e)
                result = None

            # ✅ logique propre
            if result is not None:
                result["odd_home"] = odd_home
                result["odd_draw"] = odd_draw
                result["odd_away"] = odd_away
            else:
                message = "❌ Équipe introuvable ou erreur"

        except Exception as e:
            print("INPUT ERROR:", e)
            message = "❌ Erreur dans les données entrées"

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