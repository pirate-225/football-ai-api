import pandas as pd

print("📊 Loading matches...")

df = pd.read_csv("data_raw/all_matches.csv")

team_stats = {}

for _, row in df.iterrows():

    home = row["HomeTeam"]
    away = row["AwayTeam"]
    hg = row["FTHG"]
    ag = row["FTAG"]

    if pd.isna(hg) or pd.isna(ag):
        continue

    # init
    for team in [home, away]:
        if team not in team_stats:
            team_stats[team] = {
                "scored": 0,
                "conceded": 0,
                "points": 0,
                "games": 0
            }

    # update
    team_stats[home]["scored"] += hg
    team_stats[home]["conceded"] += ag
    team_stats[home]["games"] += 1

    team_stats[away]["scored"] += ag
    team_stats[away]["conceded"] += hg
    team_stats[away]["games"] += 1

    # points
    if hg > ag:
        team_stats[home]["points"] += 3
    elif hg < ag:
        team_stats[away]["points"] += 3
    else:
        team_stats[home]["points"] += 1
        team_stats[away]["points"] += 1


print("⚙️ Building team stats...")

rows = []

for team, s in team_stats.items():

    if s["games"] < 5:
        continue

    goals_avg = s["scored"] / s["games"]
    conceded_avg = s["conceded"] / s["games"]
    ppg = s["points"] / s["games"]

    # 🔥 ELO simple
    elo = 1000 + (ppg * 100)

    rows.append({
        "Team": team,
        "GoalsScoredAvg": round(goals_avg, 2),
        "GoalsConcededAvg": round(conceded_avg, 2),
        "PPG": round(ppg, 2),
        "ELO": round(elo, 0)
    })

df_out = pd.DataFrame(rows)

df_out.to_csv("data_processed/team_stats.csv", index=False)

print("✅ DONE")
print("Teams:", len(df_out))