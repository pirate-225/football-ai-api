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
    "Norway", "Sweden", "Poland", "Czech Republic",
    "Brazil", "Argentina", "Chile", "Colombia",
    "USA", "Mexico", "Costa Rica", "Ecuador", "Paraguay",
    "Japan", "South Korea", "Bolivia", "Ireland",
    "Morocco", "Egypt", "Algeria", "South Africa",
    "Australia", "Azerbaijan", "Northern Ireland",
    "Croatia", "Greece", "Cyprus", "Finland",
    "Faroe Islands", "Iceland", "Lithuania", "Peru",
    "Serbia", "Slovakia", "Venezuela", "Wales",
    "Belarus", "Russia", "Israel", "Saudi Arabia",
    "Georgia", "Romania", "Uruguay", "China", "Canada", 
    "Latvia", "Jamaica", "Costa Rica"
]


# 🌍 Filtre pays
leagues_df = leagues_df[leagues_df["country"].isin(important_countries)]

# ⚡ Garder seulement 2 ligues max par pays (D1 + D2)
leagues_df = leagues_df.sort_values("league_id").groupby("country").head(2)

# 🌍 Compétitions internationales importantes
important_leagues_extra = [
    2,   # Champions League
    3,   # Europa League
    848, # Conference League
    1,   # World Cup
    4,   # Euro
    6    # Africa Cup
]

# 🔥 LISTE COMPLETE (TOUT CE QUE TU AS DEMANDÉ)
LEAGUES = [

    # 🌍 INTERNATIONALES
    1, 4, 6, 5, 2, 3, 848,

    # 🇬🇧
    39, 40, 41,

    # 🇪🇺 TOP
    61, 140, 135, 78, 88, 94, 144, 203, 207, 218,

    # 🌍 AMERIQUE
    71, 128, 265, 239, 253, 262, 218, 242, 281, 98,

    # 🌏 ASIE / OCEANIE
    292, 293, 98, 188,

    # 🌍 AFRIQUE
    201, 202, 233, 288,

    # 🌍 EURO SECOND
    113, 29, 4, 346, 119, 345,

    # 🌍 AUTRES
    365, 475, 252, 300, 332,

    # 🇩🇪 REGIONALLIGA
    1046, 1047, 1048,

    # 🇧🇷 U20
    1234,

    # 🇺🇸 USL
    489, 490
]


print("Total ligues sélectionnées :", len(leagues_df))

all_matches = []

# 🎯 SAISONS UNIQUEMENT
seasons = [2025, 2026]

# 1️⃣ Ligues nationales
for _, row in leagues_df.iterrows():
    league_id = row["league_id"]
    league_name = row["league_name"]
    country = row["country"]

    for season in seasons:
        print(f"Downloading {league_name} ({country}) - {season}")

        url = "https://v3.football.api-sports.io/fixtures"

        params = {
            "league": league_id,
            "season": season
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            fixtures = data.get("response", [])

            for f in fixtures:
                all_matches.append({
                    "fixture_id": f["fixture"]["id"],
                    "date": f["fixture"]["date"],
                    "HomeTeam": f["teams"]["home"]["name"],
                    "AwayTeam": f["teams"]["away"]["name"],
                    "FTHG": f["goals"]["home"],
                    "FTAG": f["goals"]["away"],
                    "league_id": league_id,
                    "league_name": league_name,
                    "country": country,
                    "season": season
                })

            time.sleep(0.5)

        except Exception as e:
            print("Erreur:", league_name, e)

# 2️⃣ Compétitions internationales
for league_id in important_leagues_extra:
    for season in seasons:
        print(f"Downloading INTERNATIONAL league {league_id} - {season}")

        url = "https://v3.football.api-sports.io/fixtures"

        params = {
            "league": league_id,
            "season": season
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            fixtures = data.get("response", [])

            for f in fixtures:
                all_matches.append({
                    "fixture_id": f["fixture"]["id"],
                    "date": f["fixture"]["date"],
                    "HomeTeam": f["teams"]["home"]["name"],
                    "AwayTeam": f["teams"]["away"]["name"],
                    "FTHG": f["goals"]["home"],
                    "FTAG": f["goals"]["away"],
                    "league_id": league_id,
                    "league_name": "International",
                    "country": "World",
                    "season": season
                })

            time.sleep(0.5)

        except Exception as e:
            print("Erreur international:", e)

# 💾 Sauvegarde
df = pd.DataFrame(all_matches)

os.makedirs("data_raw", exist_ok=True)
df.to_csv("data_raw/api_matches_all_leagues.csv", index=False)

print("✅ Download terminé")
print("Matchs total :", len(df))