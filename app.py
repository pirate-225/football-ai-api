from flask import Flask, render_template, request
import pandas as pd
import os
import requests
from data_api import (
    get_live_data,
    get_team_stats,
    get_team_form,
    get_team_stats_advanced,
    get_team_xg,
    get_team_possession
)
from data_api import get_team_form
from data_api import get_team_shots
from data_api import get_team_possession

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

    top_bets = []

    result = None
    message = None

    # 🔥 LIVE DATA (FIX: AVANT UTILISATION)
    try:
        live_data = get_live_data()[:20]  # 🔥 LIMITE À 20 MATCHS
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

            form_home = 1.5
            form_away = 1.5

            adv_home = {"shots": 3, "possession": 50}
            adv_away = {"shots": 3, "possession": 50}

            shots_home = 5
            shots_away = 5

            pos_home = 50
            pos_away = 50

            for m in live_data:
                if home.lower() in m["home"].lower() and away.lower() in m["away"].lower():

                    stats_home = get_team_stats(m["home_id"], m["league_id"], m["season"])
                    stats_away = get_team_stats(m["away_id"], m["league_id"], m["season"])

                    form_home = get_team_form(m["home_id"])
                    form_away = get_team_form(m["away_id"])

                    shots_home = get_team_shots(m["home_id"])
                    shots_away = get_team_shots(m["away_id"])

                    pos_home = get_team_possession(m["home_id"])
                    pos_away = get_team_possession(m["away_id"])

                    xg_home = get_team_xg(m["home_id"])
                    xg_away = get_team_xg(m["away_id"])

                    break

            print("FOUND MATCH:", stats_home is not None)

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
                    stats_away,
                    form_home,
                    form_away,
                    shots_home,
                    shots_away,
                    pos_home,
                    pos_away,
                    xg_home,
                    xg_away
                )

                if result:
                    result["odd_home"] = odd_home
                    result["odd_draw"] = odd_draw
                    result["odd_away"] = odd_away

        except Exception as e:
            import traceback
            traceback.print_exc()
            message = "❌ Erreur"

        # 🔥 TOP BETS (fix crash)
        top_bets = []

        try:
            top_bets = []

            if len(live_data) > 0:
                top_bets = get_top_bets(live_data[:10])  # 🔥 sécurité
            print("TOP BETS:", top_bets)
        except Exception as e:
            print("TOP BETS ERROR:", e)

    return render_template(
        "index.html",
        teams=teams,
        result=result,
        top_bets=top_bets,
        message=message,
        live_matches=live_matches
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)