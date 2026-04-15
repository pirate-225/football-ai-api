import requests
import pandas as pd
import os
import time

API_KEY = os.environ.get("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


# 🔥 TES PAYS (COMPLET)
COUNTRIES = [
    "England","France","Spain","Italy","Germany","Netherlands","Portugal",
    "Belgium","Turkey","Switzerland","Austria","Scotland","Denmark","Norway",
    "Sweden","Poland","Czech Republic","Brazil","Argentina","Chile","Colombia",
    "USA","Mexico","Costa Rica","Ecuador","Paraguay","Japan","South Korea",
    "Bolivia","Ireland","Morocco","Egypt","Algeria","South Africa","Australia",
    "Azerbaijan","Northern Ireland","Cyprus","Greece","Croatia","Canada",
    "China","El Salvador","Finland","Faroe Islands","Iceland","Jamaica",
    "Lithuania","Peru","Serbia","Slovakia","Venezuela","Wales","Belarus",
    "Russia","Israel","Saudi Arabia","Georgia","Romania","Uruguay"
]


# 🔥 COMPETITIONS INTERNATIONALES
COMPETITIONS = [
    1,    # World Cup
    4,    # Euro
    7,    # CAN
    5,    # Nations League
    2,    # Champions League
    3,    # Europa League
    848   # Conference League
]


teams = set()


# 🔥 FONCTION SAFE API
def safe_request(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            return None
        return res.json()
    except:
        return None


# 🔥 1. RECUP LIGUES PAR PAYS
for country in COUNTRIES:

    print(f"🌍 {country}")

    leagues_data = safe_request(f"{BASE_URL}/leagues?country={country}")

    if not leagues_data:
        continue

    for league in leagues_data.get("response", []):

        league_id = league["league"]["id"]
        seasons = league.get("seasons", [])

        if not seasons:
            continue

        # 🔥 dernière saison dispo
        latest_season = max([s["year"] for s in seasons])

        teams_data = safe_request(
            f"{BASE_URL}/teams?league={league_id}&season={latest_season}"
        )

        if not teams_data:
            continue

        for t in teams_data.get("response", []):
            teams.add(t["team"]["name"])

        time.sleep(0.2)  # éviter blocage API


# 🔥 2. COMPETITIONS INTERNATIONALES
print("🌍 COMPETITIONS")

for comp in COMPETITIONS:

    teams_data = safe_request(f"{BASE_URL}/teams?league={comp}")

    if not teams_data:
        continue

    for t in teams_data.get("response", []):
        teams.add(t["team"]["name"])

    time.sleep(0.2)


# 🔥 SECURITE ANTI-VIDE
if len(teams) < 100:
    print("❌ ERREUR: trop peu d’équipes → on garde l’ancien fichier")
else:

    df = pd.DataFrame({
        "Team": list(teams),
        "GoalsScoredAvg": 1.2,
        "GoalsConcededAvg": 1.2,
        "PPG": 1.3
    })

    df.to_csv("data_processed/team_stats.csv", index=False)

    print(f"✅ SUCCESS: {len(df)} équipes ajoutées")