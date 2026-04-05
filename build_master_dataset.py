import pandas as pd

print("Lecture matches...")
matches = pd.read_csv("data_raw/api_matches_all_leagues.csv")

print("Lecture odds...")
odds = pd.read_csv("data_raw/api_odds.csv")

print("Lecture standings...")
standings = pd.read_csv("data_raw/api_standings.csv")

# Renommer colonnes
matches = matches.rename(columns={
    "date": "Date",
    "home_team": "HomeTeam",
    "away_team": "AwayTeam",
    "home_goals": "FTHG",
    "away_goals": "FTAG"
})

# Merge odds
dataset = matches.merge(odds, left_on="fixture_id", right_on="fixture_id", how="left")

# Merge standings home
dataset = dataset.merge(
    standings,
    left_on="HomeTeam",
    right_on="team",
    how="left"
)

dataset = dataset.rename(columns={
    "position": "home_position",
    "points": "home_points"
})

# Merge standings away
dataset = dataset.merge(
    standings,
    left_on="AwayTeam",
    right_on="team",
    how="left"
)

dataset = dataset.rename(columns={
    "position": "away_position",
    "points": "away_points"
})

dataset.to_csv("data_processed/master_dataset.csv", index=False)

print("master_dataset.csv créé !")