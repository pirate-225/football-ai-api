import pandas as pd
import os

print("Building team stats...")

matches = pd.read_csv("data_processed/master_dataset.csv")

# ⚠️ garder saison récente
matches = matches[matches["season"].isin([2024, 2025])]

teams = pd.unique(matches[["HomeTeam", "AwayTeam"]].values.ravel())

stats = []

for team in teams:
    home = matches[matches["HomeTeam"] == team]
    away = matches[matches["AwayTeam"] == team]

    all_matches = pd.concat([home, away])

    if len(all_matches) < 10:
        continue

    # 🔥 derniers matchs (form)
    last = all_matches.sort_values("date").tail(5)

    goals_scored = 0
    goals_conceded = 0
    points = 0

    for _, m in last.iterrows():
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

    form = points / 15

    # 🔥 stats globales
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

    ppg = total_points / total_matches

    # 🔥 nouvelles features CRUCIALES
    goals_scored_avg = goals_scored / len(last)
    goals_conceded_avg = goals_conceded / len(last)

    stats.append({
        "Team": team,
        "PointsPerGame": ppg,
        "Form": form,
        "GoalsScoredAvg": goals_scored_avg,
        "GoalsConcededAvg": goals_conceded_avg,
        "MatchesPlayed": total_matches
    })

df = pd.DataFrame(stats)

os.makedirs("data_processed", exist_ok=True)
df.to_csv("data_processed/team_stats.csv", index=False)

print("team_stats.csv created")