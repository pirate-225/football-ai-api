import requests
import datetime

API_KEY = "3b63a56a290a3bd3d4b00c5b232d37d3"

HEADERS = {
    "x-apisports-key": API_KEY
}

# =========================
# 🔥 MATCHS DU JOUR
# =========================
def get_live_data():

    print("API CALL: get_live_data()")

    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "date": datetime.date.today().strftime("%Y-%m-%d")
    }

    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=5).json()

        matches = []

        for f in res.get("response", []):

            matches.append({
                "home": f["teams"]["home"]["name"],
                "away": f["teams"]["away"]["name"],
                "home_goals": f["goals"]["home"],
                "away_goals": f["goals"]["away"],
                "league": f["league"]["name"],
                "home_id": f["teams"]["home"]["id"],
                "away_id": f["teams"]["away"]["id"],
                "league_id": f["league"]["id"],
                "season": f["league"]["season"]
            })

        print("LIVE MATCHES COUNT:", len(matches))

        return matches

    except Exception as e:
        print("API ERROR (live):", e)
        return []


# =========================
# 🔥 FORM (5 DERNIERS MATCHS)
# =========================
def get_team_form(team_id):

    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "team": team_id,
        "last": 5
    }

    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=5).json()

        points = 0

        for f in res.get("response", []):

            gh = f["goals"]["home"]
            ga = f["goals"]["away"]

            if gh is None:
                continue

            # ⚠️ simplification (on ne distingue pas home/away ici)
            if gh > ga:
                points += 3
            elif gh == ga:
                points += 1

        form = points / 5

        return form

    except Exception as e:
        print("API ERROR (form):", e)
        return 1.5


# =========================
# 🔥 STATS ÉQUIPE (ATT / DEF)
# =========================
def get_team_stats(team_id, league_id, season):

    url = "https://v3.football.api-sports.io/teams/statistics"

    params = {
        "team": team_id,
        "league": league_id,
        "season": season
    }

    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=5).json()

        data = res.get("response", {})

        attack = float(data["goals"]["for"]["average"]["total"])
        defense = float(data["goals"]["against"]["average"]["total"])

        return {
            "attack": attack,
            "defense": defense
        }

    except Exception as e:
        print("API ERROR (stats):", e)
        return {
            "attack": 1.2,
            "defense": 1.2
        }