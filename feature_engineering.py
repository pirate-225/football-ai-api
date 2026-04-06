import pandas as pd

print("Lecture matchs API...")
matches = pd.read_csv("data_processed/master_dataset.csv")

print("Création des features...")

# Points per game
matches["home_points_per_game"] = matches["home_points"] / 38
matches["away_points_per_game"] = matches["away_points"] / 38

# Goal diff
matches["home_goal_diff"] = matches["FTHG"] - matches["FTAG"]
matches["away_goal_diff"] = matches["FTAG"] - matches["FTHG"]

# Diff features
matches["points_diff"] = matches["home_points_per_game"] - matches["away_points_per_game"]
matches["goal_diff_diff"] = matches["home_goal_diff"] - matches["away_goal_diff"]
matches["position_diff"] = matches["home_position"] - matches["away_position"]
matches["elo_diff"] = matches["elo_home"] - matches["elo_away"]
matches["form_diff"] = matches["home_form"] - matches["away_form"]

# Targets
def get_result(row):
    if row["FTHG"] > row["FTAG"]:
        return 0
    elif row["FTHG"] == row["FTAG"]:
        return 1
    else:
        return 2

matches["result"] = matches.apply(get_result, axis=1)
matches["over25"] = ((matches["FTHG"] + matches["FTAG"]) > 2).astype(int)
matches["btts"] = ((matches["FTHG"] > 0) & (matches["FTAG"] > 0)).astype(int)

features = matches[[
    "home_points_per_game",
    "away_points_per_game",
    "points_diff",
    "goal_diff_diff",
    "position_diff",
    "elo_diff",
    "form_diff",
    "result",
    "over25",
    "btts"
]]

features.to_csv("data_processed/features.csv", index=False)

print("features.csv créé !")