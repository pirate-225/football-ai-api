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

    import datetime

    url = "https://v3.football.api-sports.io/fixtures"

    headers = {
        "x-apisports-key": "3b63a56a290a3bd3d4b00c5b232d37d3"
    }

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    params = {
        "date": today,
        "timezone": "Europe/Paris"
    }

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5).json()

        data = []

        for f in res.get("response", []):

            data.append({
                "home": f["teams"]["home"]["name"],
                "away": f["teams"]["away"]["name"],
                "home_goals": f["goals"]["home"],
                "away_goals": f["goals"]["away"],
                "league": f["league"]["name"],
                "home_id": f["teams"]["home"]["id"],
                "away_id": f["teams"]["away"]["id"],
                "league_id": f["league"]["id"],
                "season": f["league"]["season"],
                "fixture_id": f["fixture"]["id"],
                "status": f["fixture"]["status"]["short"]
            })

        print("TOTAL FIXTURES:", len(data))
        return data

    except Exception as e:
        print("API ERROR:", e)
        return []

    params = {
        "live": "all"
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

def get_match_stats(fixture_id):

    url = "https://v3.football.api-sports.io/fixtures/statistics"
    headers = {"x-apisports-key": API_KEY}

    params = {"fixture": fixture_id}

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5).json()

        stats = {"home": {}, "away": {}}

        for i, team in enumerate(res.get("response", [])):
            side = "home" if i == 0 else "away"

            for s in team["statistics"]:

                if s["type"] == "Total Shots":
                    stats[side]["shots"] = int(s["value"] or 0)

                if s["type"] == "Ball Possession":
                    stats[side]["possession"] = int(str(s["value"]).replace('%','') or 50)

        return stats

    except Exception as e:
        print("MATCH STATS ERROR:", e)

        return {
            "home": {"shots": 5, "possession": 50},
            "away": {"shots": 5, "possession": 50}
        }

    except:
        return {
            "shots": 3,
            "possession": 50
        }

def get_team_shots(team_id):

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

def get_odds(fixture_id):

    url = "https://v3.football.api-sports.io/odds"
    headers = {"x-apisports-key": API_KEY}

    params = {"fixture": fixture_id}

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5).json()

        for r in res.get("response", []):
            for b in r.get("bookmakers", []):
                for bet in b.get("bets", []):

                    if bet["name"] == "Match Winner":

                        odds = {}

                        for v in bet["values"]:
                            if v["value"] == "Home":
                                odds["home"] = float(v["odd"])
                            elif v["value"] == "Draw":
                                odds["draw"] = float(v["odd"])
                            elif v["value"] == "Away":
                                odds["away"] = float(v["odd"])

                        return odds

    except Exception as e:
        print("ODDS ERROR:", e)

    return None

def get_team_xg_stats(team_id, league_id, season):

    url = "https://v3.football.api-sports.io/teams/statistics"
    headers = {"x-apisports-key": API_KEY}

    params = {
        "team": team_id,
        "league": league_id,
        "season": season
    }

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5).json()

        data = res.get("response", {})

        return {
            "xg_for": data.get("goals", {}).get("for", {}).get("average", {}).get("total", 1.2),
            "xg_against": data.get("goals", {}).get("against", {}).get("average", {}).get("total", 1.2)
        }

    except:
        return {"xg_for": 1.2, "xg_against": 1.2}

def get_h2h(team1_id, team2_id):

    url = "https://v3.football.api-sports.io/fixtures/headtohead"
    headers = {"x-apisports-key": API_KEY}

    params = {
        "h2h": f"{team1_id}-{team2_id}",
        "last": 5
    }

    try:
        res = requests.get(url, headers=headers, params=params).json()

        wins_home = 0
        wins_away = 0

        for f in res.get("response", []):
            if f["goals"]["home"] > f["goals"]["away"]:
                wins_home += 1
            elif f["goals"]["away"] > f["goals"]["home"]:
                wins_away += 1

        return wins_home, wins_away

    except:
        return 0, 0
