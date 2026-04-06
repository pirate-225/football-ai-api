import pandas as pd

print("Loading matches with form and elo...")
matches = pd.read_csv("data_processed/matches_with_elo.csv")

print("Loading odds...")
odds = pd.read_csv("data_raw/api_odds.csv")

print("Loading standings...")
standings = pd.read_csv("data_raw/api_standings.csv")

# Rename
matches = matches.rename(columns={
    "date": "Date",
    "home_team": "HomeTeam",
    "away_team": "AwayTeam",
    "home_goals": "FTHG",
    "away_goals": "FTAG"
})

# Merge odds
odds = odds[["fixture_id", "home_odds", "draw_odds", "away_odds"]]
dataset = matches.merge(odds, on="fixture_id", how="left")

# Merge standings home
standings = standings[["team", "position", "points"]]

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

dataset = dataset.drop(columns=["team"])

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

dataset = dataset.drop(columns=["team"])

dataset.to_csv("data_processed/master_dataset.csv", index=False)

print("master_dataset.csv created")