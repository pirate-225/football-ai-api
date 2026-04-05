import pandas as pd
import numpy as np

print("Lecture matchs API...")
matches = pd.read_csv("data_raw/api_matches_all_leagues.csv")

print("Lecture team stats...")
team_stats = pd.read_csv("data_processed/team_stats.csv")

# Renommer colonnes API
matches = matches.rename(columns={
    "date": "Date",
    "home_team": "HomeTeam",
    "away_team": "AwayTeam",
    "home_goals": "FTHG",
    "away_goals": "FTAG"
})

# Supprimer matchs sans score
matches = matches.dropna(subset=["FTHG", "FTAG"])

# Résultat match
matches["Result"] = np.where(matches["FTHG"] > matches["FTAG"], "H",
                     np.where(matches["FTHG"] < matches["FTAG"], "A", "D"))

# Over / BTTS
matches["Over25"] = np.where(matches["FTHG"] + matches["FTAG"] > 2.5, 1, 0)
matches["BTTS"] = np.where((matches["FTHG"] > 0) & (matches["FTAG"] > 0), 1, 0)

features = []

print("Création des features...")

for index, row in matches.iterrows():
    home = row["HomeTeam"]
    away = row["AwayTeam"]

    home_stats = team_stats[team_stats["Team"] == home]
    away_stats = team_stats[team_stats["Team"] == away]

    if home_stats.empty or away_stats.empty:
        continue

    home_stats = home_stats.iloc[0]
    away_stats = away_stats.iloc[0]

    features.append({
        "home_goals_avg": home_stats["GoalsScoredAvg"],
        "away_goals_avg": away_stats["GoalsScoredAvg"],
        "home_conceded_avg": home_stats["GoalsConcededAvg"],
        "away_conceded_avg": away_stats["GoalsConcededAvg"],
        "goal_diff": home_stats["GoalDiffAvg"] - away_stats["GoalDiffAvg"],
        "Result": row["Result"],
        "Over25": row["Over25"],
        "BTTS": row["BTTS"]
    })

features_df = pd.DataFrame(features)

print("Nombre de lignes features :", len(features_df))

features_df.to_csv("data_processed/features.csv", index=False)

print("features.csv créé !")