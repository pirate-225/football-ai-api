import pandas as pd
import os

print("Building team stats...")

matches = pd.read_csv("data_processed/master_dataset.csv")

# ⚠️ utiliser uniquement saison actuelle
matches = matches[matches["season"] == 2025]

teams = pd.unique(matches[["HomeTeam", "AwayTeam"]].values.ravel())

stats = []

for team in teams:
    team_matches_home = matches[matches["HomeTeam"] == team]
    team_matches_away = matches[matches["AwayTeam"] == team]

    all_matches = pd.concat([team_matches_home, team_matches_away])

    if len(all_matches) < 5:
        continue

    # 🔥 FORM dynamique (5 derniers matchs)
    last_matches = all_matches.sort_values("date").tail(5)

    points = 0
    goals_scored = 0
    goals_conceded = 0

    for _, m in last_matches.iterrows():
        if m["HomeTeam"] == team:
            goals_scored += m["FTHG"]
            goals_conceded += m["FTAG"]

            if m["FTHG"] > m["FTAG"]:
                points += 3
            elif m["FTHG"] == m["FTAG"]:
                points += 1
        else:
            goals_scored += m["FTAG"]
            goals_conceded += m["FTHG"]

            if m["FTAG"] > m["FTHG"]:
                points += 3
            elif m["FTAG"] == m["FTHG"]:
                points += 1

    form = points / 15  # max = 15 points
    goal_diff = goals_scored - goals_conceded

    # 🔥 PPG global saison
    total_matches = len(all_matches)
    total_points = 0

    for _, m in all_matches.iterrows():
        if m["HomeTeam"] == team:
            if m["FTHG"] > m["FTAG"]:
                total_points += 3
            elif m["FTHG"] == m["FTAG"]:
                total_points += 1
        else:
            if m["FTAG"] > m["FTHG"]:
                total_points += 3
            elif m["FTAG"] == m["FTHG"]:
                total_points += 1

    ppg = total_points / total_matches if total_matches > 0 else 0

    stats.append({
        "Team": team,
        "PointsPerGame": ppg,
        "GoalDiff": goal_diff,
        "Form": form
    })

df = pd.DataFrame(stats)

os.makedirs("data_processed", exist_ok=True)
df.to_csv("data_processed/team_stats.csv", index=False)

print("team_stats.csv created")