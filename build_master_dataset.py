import pandas as pd
import os

print("Building master dataset...")

# Charger les matchs API (toutes ligues + saisons)
matches = pd.read_csv("data_raw/api_matches_all_leagues.csv")

# Nettoyage
matches = matches.dropna(subset=["HomeTeam", "AwayTeam", "FTHG", "FTAG"])

# Convertir date
matches["date"] = pd.to_datetime(matches["date"], errors="coerce")

# Trier chronologiquement
matches = matches.sort_values("date")

# Renommer colonnes pour cohérence
matches = matches.rename(columns={
    "HomeTeam": "HomeTeam",
    "AwayTeam": "AwayTeam",
    "FTHG": "FTHG",
    "FTAG": "FTAG",
    "season": "season",
    "league_id": "league_id",
    "league_name": "league_name"
})

# Garder uniquement les colonnes utiles
matches = matches[[
    "date",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "league_id",
    "league_name",
    "season"
]]

# Sauvegarde
os.makedirs("data_processed", exist_ok=True)
matches.to_csv("data_processed/master_dataset.csv", index=False)

print("master_dataset.csv created")
print("Nombre de matchs :", len(matches))