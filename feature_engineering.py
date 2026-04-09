import pandas as pd
import os

print("Building features...")

matches = pd.read_csv("data_processed/master_dataset.csv")
teams = pd.read_csv("data_processed/team_stats.csv")

features = []

# 🔥 Force des ligues (IMPORTANT)
league_strength = {
    "Spain": 1.0,
    "England": 1.0,
    "Germany": 0.95,
    "Italy": 0.95,
    "France": 0.9,
    "Netherlands": 0.85,
    "Portugal": 0.85,
    "Belgium": 0.8,
    "Turkey": 0.75,
    "Greece": 0.7,
    "Others": 0.6
}

for _, row in matches.iterrows():

    home_team = row["HomeTeam"]
    away_team = row["AwayTeam"]

    home = teams[teams["Team"] == home_team]
    away = teams[teams["Team"] == away_team]

    if home.empty or away.empty:
        continue

    home = home.iloc[0]
    away = away.iloc[0]

    # -------- FEATURES PRINCIPALES --------
    ppg_diff = home["PPG"] - away["PPG"]

    # 🔥 FILTRE MATCHS TROP ÉQUILIBRÉS
    if abs(ppg_diff) < 0.15:
        continue

    home_adv = home["HomePPG"] - away["AwayPPG"]

    form_diff = home["Form"] - away["Form"]

    attack_diff = home["GoalsScoredAvg"] - away["GoalsScoredAvg"]
    defense_diff = home["GoalsConcededAvg"] - away["GoalsConcededAvg"]

    clean_diff = home["CleanSheetRate"] - away["CleanSheetRate"]
    fail_diff = home["FailToScoreRate"] - away["FailToScoreRate"]

    elo_diff = home["ELO"] - away["ELO"]

    exp_diff = home["MatchesPlayed"] - away["MatchesPlayed"]

    # -------- 🔥 FORCE LIGUE --------
    home_country = row["country"] if "country" in row else "Others"
    away_country = row["country"] if "country" in row else "Others"

    home_league_strength = league_strength.get(home_country, 0.6)
    away_league_strength = league_strength.get(away_country, 0.6)

    league_diff = home_league_strength - away_league_strength

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
        league_diff,
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
    "league_diff",
    "result",
    "over25",
    "btts"
])

os.makedirs("data_processed", exist_ok=True)
df.to_csv("data_processed/features.csv", index=False)

print("features.csv created")