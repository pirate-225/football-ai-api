import pandas as pd
import os

print("Building features...")

matches = pd.read_csv("data_processed/master_dataset.csv")
teams = pd.read_csv("data_processed/team_stats.csv")

features = []

for _, row in matches.iterrows():

    home = teams[teams["Team"] == row["HomeTeam"]]
    away = teams[teams["Team"] == row["AwayTeam"]]

    if home.empty or away.empty:
        continue

    home = home.iloc[0]
    away = away.iloc[0]

    # -------- FEATURES --------
    ppg_diff = home["PPG"] - away["PPG"]
    home_adv = home["HomePPG"] - away["AwayPPG"]

    form_diff = home["Form"] - away["Form"]

    attack_diff = home["GoalsScoredAvg"] - away["GoalsScoredAvg"]
    defense_diff = home["GoalsConcededAvg"] - away["GoalsConcededAvg"]

    clean_diff = home["CleanSheetRate"] - away["CleanSheetRate"]
    fail_diff = home["FailToScoreRate"] - away["FailToScoreRate"]

    elo_diff = home["ELO"] - away["ELO"]

    exp_diff = home["MatchesPlayed"] - away["MatchesPlayed"]

    # -------- TARGET --------
    if row["FTHG"] > row["FTAG"]:
        result = 0
    elif row["FTHG"] == row["FTAG"]:
        result = 1
    else:
        result = 2

    over25 = 1 if (row["FTHG"] + row["FTAG"]) > 2 else 0
    btts = 1 if (row["FTHG"] > 0 and row["FTAG"] > 0) else 0

    features.append([
        ppg_diff,
        home_adv,
        form_diff,
        attack_diff,
        defense_diff,
        clean_diff,
        fail_diff,
        elo_diff,
        exp_diff,
        result,
        over25,
        btts
    ])

df = pd.DataFrame(features, columns=[
    "ppg_diff",
    "home_adv",
    "form_diff",
    "attack_diff",
    "defense_diff",
    "clean_diff",
    "fail_diff",
    "elo_diff",
    "exp_diff",
    "result",
    "over25",
    "btts"
])

os.makedirs("data_processed", exist_ok=True)
df.to_csv("data_processed/features.csv", index=False)

print("features.csv created")