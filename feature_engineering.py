import pandas as pd
import os

print("Building features...")

matches = pd.read_csv("data_processed/master_dataset.csv")
teams = pd.read_csv("data_processed/team_stats.csv")

features = []

for _, row in matches.iterrows():

    home_team = row["HomeTeam"]
    away_team = row["AwayTeam"]

    home = teams[teams["Team"] == home_team]
    away = teams[teams["Team"] == away_team]

    if home.empty or away.empty:
        continue

    home = home.iloc[0]
    away = away.iloc[0]

    # 🔥 variables
    home_ppg = home["PointsPerGame"]
    away_ppg = away["PointsPerGame"]

    home_form = home["Form"]
    away_form = away["Form"]

    home_attack = home["GoalsScoredAvg"]
    away_attack = away["GoalsScoredAvg"]

    home_defense = home["GoalsConcededAvg"]
    away_defense = away["GoalsConcededAvg"]

    home_exp = home["MatchesPlayed"]
    away_exp = away["MatchesPlayed"]

    # 🔥 différences
    ppg_diff = home_ppg - away_ppg
    form_diff = home_form - away_form
    attack_diff = home_attack - away_attack
    defense_diff = home_defense - away_defense
    exp_diff = home_exp - away_exp

    # 🔥 strength pondérée (IMPORTANT)
    strength_home = home_ppg * 0.7 + home_attack * 0.3
    strength_away = away_ppg * 0.7 + away_attack * 0.3
    strength_diff = strength_home - strength_away

    # target
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
        ppg_diff,
        form_diff,
        attack_diff,
        defense_diff,
        strength_diff,
        exp_diff,
        result,
        over25,
        btts
    ])

df = pd.DataFrame(features, columns=[
    "home_ppg",
    "away_ppg",
    "ppg_diff",
    "form_diff",
    "attack_diff",
    "defense_diff",
    "strength_diff",
    "exp_diff",
    "result",
    "over25",
    "btts"
])

os.makedirs("data_processed", exist_ok=True)
df.to_csv("data_processed/features.csv", index=False)

print("features.csv created")