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
                "season": f["league"]["season"],
                "fixture_id": f["fixture"]["id"]  # 🔥 AJOUT ICI
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

def get_team_form(team_id):

    url = "https://v3.football.api-sports.io/fixtures"

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "team": team_id,
        "last": 5
    }

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5).json()

        points = 0
        goals_for = 0
        goals_against = 0

        for f in res.get("response", []):

            gh = f["goals"]["home"]
            ga = f["goals"]["away"]

            if gh is None:
                continue

            goals_for += gh
            goals_against += ga

            if gh > ga:
                points += 3
            elif gh == ga:
                points += 1

        return {
            "form": points / 5,
            "attack": goals_for / 5,
            "defense": goals_against / 5
        }

    except Exception as e:
        print("FORM API ERROR:", e)
        return {
            "form": 1.5,
            "attack": 1.2,
            "defense": 1.2
        }

def get_team_stats_advanced(team_id):

    url = "https://v3.football.api-sports.io/fixtures/statistics"

    headers = {
        "x-apisports-key": API_KEY
    }

    try:
        res = requests.get(url, headers=headers, timeout=5).json()

        shots_on_target = 0
        possession = 0

        for team in res.get("response", []):

            if team["team"]["id"] == team_id:

                for stat in team["statistics"]:

                    if stat["type"] == "Shots on Goal":
                        shots_on_target = float(stat["value"] or 0)

                    if stat["type"] == "Ball Possession":
                        possession = float(stat["value"].replace('%','') or 50)

        return {
            "shots": shots_on_target,
            "possession": possession
        }

    except:
        return {
            "shots": 3,
            "possession": 50
        }

def get_team_shots(team_id):
    return 5

    url = "https://v3.football.api-sports.io/teams/statistics"

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "team": team_id,
        "season": 2026
    }

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5).json()

        shots = res["response"]["shots"]["on"]

        return shots or 5

    except:
        return 5

def get_team_possession(team_id):
    return 50

    url = "https://v3.football.api-sports.io/teams/statistics"

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "team": team_id,
        "season": 2026
    }

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5).json()

        possession = res["response"]["fixtures"]["played"]["total"]

        # fallback simple (évite crash)
        return possession or 50

    except:
        return 50

def get_team_xg(team_id):

    url = "https://v3.football.api-sports.io/teams/statistics"

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "team": team_id,
        "season": 2026
    }

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5).json()

        goals = res["response"]["goals"]["for"]["total"]["total"]

        matches = res["response"]["fixtures"]["played"]["total"]

        return goals / max(matches, 1)

    except:
        return 1.2

def get_match_odds(fixture_id):

    url = "https://v3.football.api-sports.io/odds"

    params = {
        "fixture": fixture_id
    }

    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=3).json()

        bookmakers = res.get("response", [])

        for b in bookmakers:
            for bet in b.get("bookmakers", []):
                for market in bet.get("bets", []):

                    if market["name"] == "Match Winner":

                        values = market["values"]

                        odds = {}

                        for v in values:
                            if v["value"] == "Home":
                                odds["home"] = float(v["odd"])
                            elif v["value"] == "Draw":
                                odds["draw"] = float(v["odd"])
                            elif v["value"] == "Away":
                                odds["away"] = float(v["odd"])

                        if len(odds) == 3:
                            return odds

        return None

    except Exception as e:
        print("ODDS API ERROR:", e)
        return None