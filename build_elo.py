import pandas as pd
import math

print("Loading matches...")
matches = pd.read_csv("data_processed/matches_with_form.csv")

teams = pd.concat([matches["home_team"], matches["away_team"]]).unique()

elo = {team: 1500 for team in teams}

elo_home = []
elo_away = []

K = 20

for index, row in matches.iterrows():
    home = row["home_team"]
    away = row["away_team"]

    elo_home.append(elo[home])
    elo_away.append(elo[away])

    hg = row["home_goals"]
    ag = row["away_goals"]

    if hg > ag:
        result_home = 1
    elif hg < ag:
        result_home = 0
    else:
        result_home = 0.5

    expected_home = 1 / (1 + 10 ** ((elo[away] - elo[home]) / 400))

    elo[home] = elo[home] + K * (result_home - expected_home)
    elo[away] = elo[away] + K * ((1 - result_home) - (1 - expected_home))

matches["elo_home"] = elo_home
matches["elo_away"] = elo_away

matches.to_csv("data_processed/matches_with_elo.csv", index=False)

print("Elo added")