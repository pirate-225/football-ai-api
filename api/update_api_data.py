import requests
import pandas as pd
import os
import time

API_KEY = "3b63a56a290a3bd3d4b00c5b232d37d3"

headers = {
    "x-apisports-key": API_KEY
}

print("Loading leagues...")

leagues_df = pd.read_csv("data_raw/leagues.csv")

# 🌍 Pays que TU veux (liste complète)
important_countries = [
    "England", "France", "Spain", "Italy", "Germany",
    "Netherlands", "Portugal", "Belgium", "Turkey",
    "Switzerland", "Austria", "Scotland", "Denmark",
    "Norway", "Sweden", "Poland", "Czech-Republic",
    "Brazil", "Argentina", "Chile", "Colombia", 
    "USA", "Mexico", "Costa-Rica", "Ecuador", "Paraguay",
    "Japan", "South-Korea", "Bolivia", "Ireland", 
    "Morocco", "Egypt", "Algeria", "England-League-One",
    "Australia", "Azerbaijan", "Estonia", "World-Cup", 
    "Croatia", "Greece", "Cyprus", "Finland",
    "Faroe-Islands", "Iceland", "Lithuania", "Peru", "Bulgaria",
    "Serbia", "Slovakia", "Venezuela", "Wales", 
    "Belarus", "Russia", "Israel", "Saudi-Arabia",
    "Georgia", "Romania", "Uruguay", "China", "Canada", 
    "Latvia", "Jamaica", "El-Salvador", "Northern-Ireland"
]


# 🌍 FILTRE
leagues_df = leagues_df[leagues_df["country"].isin(important_countries)]

# ⚡ D1 + D2
leagues_df = leagues_df.sort_values("league_id").groupby("country").head(2)


# 🔥 LIGUES SUPPLÉMENTAIRES (TES DEMANDES EXACTES)
extra_leagues = [
    489,  # USL Championship
    490,  # USL League One
    2,    # Champions League
    3,    # Europa League
    848,  # Conference League
    1,    # World Cup
    4,    # Euro
    5,    # Nations League
    6,    # Africa Cup
    41    # England League One
]


print("Total ligues nationales :", len(leagues_df))


all_matches = []

seasons = [2025, 2026]


# 🔥 FONCTION SAFE
def get_fixtures(league_id, season, name, country):

    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "league": league_id,
        "season": season
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            return []

        data = response.json()
        return data.get("response", [])

    except:
        return []


# 1️⃣ LIGUES NATIONALES
for _, row in leagues_df.iterrows():

    league_id = row["league_id"]
    league_name = row["league_name"]
    country = row["country"]

    for season in seasons:

        print(f"📊 {league_name} ({country}) - {season}")

        fixtures = get_fixtures(league_id, season, league_name, country)

        for f in fixtures:

            hg = f["goals"]["home"]
            ag = f["goals"]["away"]

            if hg is None or ag is None:
                continue

            all_matches.append({
                "fixture_id": f["fixture"]["id"],
                "date": f["fixture"]["date"],
                "HomeTeam": f["teams"]["home"]["name"],
                "AwayTeam": f["teams"]["away"]["name"],
                "FTHG": hg,
                "FTAG": ag,
                "league_id": league_id,
                "league_name": league_name,
                "country": country,
                "season": season
            })

        time.sleep(0.4)


# 2️⃣ TES LIGUES SPÉCIALES
print("🌍 EXTRA LEAGUES")

for league_id in extra_leagues:

    for season in seasons:

        print(f"📊 Extra League {league_id} - {season}")

        fixtures = get_fixtures(league_id, season, f"League {league_id}", "Custom")

        for f in fixtures:

            hg = f["goals"]["home"]
            ag = f["goals"]["away"]

            if hg is None or ag is None:
                continue

            all_matches.append({
                "fixture_id": f["fixture"]["id"],
                "date": f["fixture"]["date"],
                "HomeTeam": f["teams"]["home"]["name"],
                "AwayTeam": f["teams"]["away"]["name"],
                "FTHG": hg,
                "FTAG": ag,
                "league_id": league_id,
                "league_name": f["league"]["name"],
                "country": f["league"]["country"],
                "season": season
            })

        time.sleep(0.4)


# 💾 SAVE
df = pd.DataFrame(all_matches)

os.makedirs("data_raw", exist_ok=True)
df.to_csv("data_raw/api_matches_all_leagues.csv", index=False)

print("✅ DONE")
print("Matchs total :", len(df))