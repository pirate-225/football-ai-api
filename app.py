from flask import Flask, render_template, request
import pandas as pd
import os
import requests
from data_api import get_live_data, get_team_stats

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

        res = requests.get(url, headers=headers, params=params, timeout=5).json()

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

    result = None
    message = None

    # 🔥 LIVE DATA (FIX: AVANT UTILISATION)
    try:
        live_data = get_live_data()
        print("LIVE DATA:", live_data[:2])
    except Exception as e:
        print("LIVE DATA ERROR:", e)
        live_data = []

    # 🔥 LIVE MATCHES
    try:
        live_matches = get_live_matches()[:10]
    except Exception as e:
        print("LIVE ERROR:", e)
        live_matches = []

    # 🔥 PREDICTION
    if request.method == "POST":

        try:
            home = request.form.get("home_team")
            away = request.form.get("away_team")

            odd_home = float(request.form.get("odd_home") or 0)
            odd_draw = float(request.form.get("odd_draw") or 0)
            odd_away = float(request.form.get("odd_away") or 0)

            print("MATCH INPUT:", home, away)
            print("LIVE MATCHES:", live_data[:3])

            stats_home = None
            stats_away = None

            for m in live_data:
                if home.lower() in m["home"].lower() and away.lower() in m["away"].lower():
                    stats_home = get_team_stats(m["home_id"], m["league_id"], m["season"])
                    stats_away = get_team_stats(m["away_id"], m["league_id"], m["season"])
                    break

            if stats_home is None or stats_away is None:
                result = None
                message = "❌ Match non trouvé dans API"
            else:
                result = predict_match(
                    home,
                    away,
                    odd_home,
                    odd_draw,
                    odd_away,
                    stats_home,
                    stats_away
                )

                if result:
                    result["odd_home"] = odd_home
                    result["odd_draw"] = odd_draw
                    result["odd_away"] = odd_away

        except Exception as e:
            print("PREDICT ERROR:", e)
            message = "❌ Erreur"

    return render_template(
        "index.html",
        teams=teams,
        result=result,
        top_bets=[],
        message=message,
        live_matches=live_matches
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)