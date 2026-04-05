import pandas as pd

print("Loading matches...")
matches = pd.read_csv("data_raw/api_matches_all_leagues.csv")

print("Loading odds...")
odds = pd.read_csv("data_raw/api_odds.csv")

print("Loading standings...")
standings = pd.read_csv("data_raw/api_standings.csv")

# Rename matches columns
matches = matches.rename(columns={
    "date": "Date",
    "home_team": "HomeTeam",
    "away_team": "AwayTeam",
    "home_goals": "FTHG",
    "away_goals": "FTAG"
})

# Keep only useful columns in odds
odds = odds[[
    "fixture_id",
    "home_odds",
    "draw_odds",
    "away_odds"
]]

# Keep only useful columns in standings
standings = standings[[
    "team",
    "position",
    "points"
]]

print("Merging odds...")
dataset = matches.merge(odds, on="fixture_id", how="left")

print("Merging home standings...")
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

print("Merging away standings...")
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

# Diff features
dataset["position_diff"] = dataset["home_position"] - dataset["away_position"]
dataset["odds_diff"] = dataset["home_odds"] - dataset["away_odds"]
dataset["goals_diff"] = dataset["FTHG"] - dataset["FTAG"]

dataset.to_csv("data_processed/master_dataset.csv", index=False)

print("master_dataset.csv created successfully")