import requests
import pandas as pd
import os

API_KEY = os.environ.get("API_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"

# 🔥 TOUTES TES LIGUES (COMPLET)
LEAGUES = [

    # 🇬🇧
    41,   # League One

    # 🇬🇧 Irlande du Nord
    332,  # NIFL Premiership

    # 🇸🇻 Salvador
    345,  # Primera Division

    # 🇯🇲 Jamaïque
    475,  # Premier League

    # 🇱🇻 Lettonie
    365,  # Virsliga

    # 🇨🇷 Costa Rica
    218,  # Primera Division

    # 🇰🇷 Corée
    292,  # K League 1
    293,  # K League 2

    # 🇺🇸 USA
    489,  # USL Championship
    490,  # USL League One

    # 🇫🇴 Îles Féroé
    252,  # Premier League

    # 🇨🇦 Canada
    300,  # Canadian Premier League

    # 🇩🇪 Allemagne (Regionalliga)
    1046, # Regionalliga Nordost
    1047, # Regionalliga West
    1048, # Regionalliga North

    # 🇧🇷 Brésil U20
    1234  # Brasileiro U20 (⚠️ peut varier selon API)
]

teams = set()

for league in LEAGUES:

    try:
        url = f"{BASE_URL}/teams?league={league}&season=2024"
        res = requests.get(url, headers=HEADERS, timeout=5).json()

        for t in res.get("response", []):
            teams.add(t["team"]["name"])

    except Exception as e:
        print("Error league:", league, e)
        continue


# 🔥 DATASET
df = pd.DataFrame({
    "Team": list(teams),
    "GoalsScoredAvg": 1.2,
    "GoalsConcededAvg": 1.2,
    "PPG": 1.3
})

df.to_csv("data_processed/team_stats.csv", index=False)

print("✅ Teams added:", len(df))