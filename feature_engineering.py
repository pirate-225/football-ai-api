import pandas as pd
import os

print("Building features...")

matches = pd.read_csv("data_processed/master_dataset.csv")
teams = pd.read_csv("data_processed/team_stats.csv")

features = []

for index, row in matches.iterrows():

    home_team = row["HomeTeam"]
    away_team = row["AwayTeam"]

    home = teams[teams["Team"] == home_team]
    away = teams[teams["Team"] == away_team]

    if home.empty or away.empty:
        continue

    home = home.iloc[0]
    away = away.iloc[0]

    home_ppg = home["PointsPerGame"]
    away_ppg = away["PointsPerGame"]

    home_goal_diff = home["GoalDiff"]
    away_goal_diff = away["GoalDiff"]

    home_form = home["Form"]
    away_form = away["Form"]

    home_elo = home["Elo"]
    away_elo = away["Elo"]

    home_pos = home["Position"]
    away_pos = away["Position"]

    result = 0
    if row["FTHG"] > row["FTAG"]:
        result = 0
    elif row["FTHG"] == row["FTAG"]:
        result = 1
    else:
        result = 2

    over25 = 1 if (row["FTHG"] + row["FTAG"]) > 2 else 0
    btts = 1 if (row["FTHG"] > 0 and row["FTAG"] > 0) else 0

    features.append([
        home_ppg,
        away_ppg,
        home_ppg - away_ppg,
        home_goal_diff - away_goal_diff,
        home_pos - away_pos,
        home_elo - away_elo,
        home_form - away_form,
        result,
        over25,
        btts
    ])

df = pd.DataFrame(features, columns=[
    "home_ppg",
    "away_ppg",
    "ppg_diff",
    "goal_diff_diff",
    "position_diff",
    "elo_diff",
    "form_diff",
    "result",
    "over25",
    "btts"
])

os.makedirs("data_processed", exist_ok=True)
df.to_csv("data_processed/features.csv", index=False)

print("features.csv created")