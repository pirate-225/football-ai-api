import pandas as pd

df = pd.read_csv("data_raw/api_matches_all_leagues.csv")

team_stats = {}

def init_team(team):
    return {
        "scored": 0,
        "conceded": 0,
        "points": 0,
        "games": 0,
        "recent_points": [],
        "home_scored": 0,
        "home_conceded": 0,
        "home_games": 0,
        "away_scored": 0,
        "away_conceded": 0,
        "away_games": 0
    }

for _, row in df.iterrows():

    home = row["HomeTeam"]
    away = row["AwayTeam"]
    hg = row["FTHG"]
    ag = row["FTAG"]

    if pd.isna(hg) or pd.isna(ag):
        continue

    if home not in team_stats:
        team_stats[home] = init_team(home)
    if away not in team_stats:
        team_stats[away] = init_team(away)

    # global stats
    team_stats[home]["scored"] += hg
    team_stats[home]["conceded"] += ag
    team_stats[home]["games"] += 1

    team_stats[away]["scored"] += ag
    team_stats[away]["conceded"] += hg
    team_stats[away]["games"] += 1

    # home/away split
    team_stats[home]["home_scored"] += hg
    team_stats[home]["home_conceded"] += ag
    team_stats[home]["home_games"] += 1

    team_stats[away]["away_scored"] += ag
    team_stats[away]["away_conceded"] += hg
    team_stats[away]["away_games"] += 1

    # points
    if hg > ag:
        hp, ap = 3, 0
    elif hg < ag:
        hp, ap = 0, 3
    else:
        hp, ap = 1, 1

    team_stats[home]["points"] += hp
    team_stats[away]["points"] += ap

    # recent form (last 5)
    team_stats[home]["recent_points"].append(hp)
    team_stats[away]["recent_points"].append(ap)

    team_stats[home]["recent_points"] = team_stats[home]["recent_points"][-5:]
    team_stats[away]["recent_points"] = team_stats[away]["recent_points"][-5:]

rows = []

for team, s in team_stats.items():

    if s["games"] < 5:
        continue

    goals_avg = s["scored"] / s["games"]
    conceded_avg = s["conceded"] / s["games"]

    ppg = s["points"] / s["games"]
    form = sum(s["recent_points"]) / max(len(s["recent_points"]), 1)

    home_attack = s["home_scored"] / max(s["home_games"], 1)
    away_attack = s["away_scored"] / max(s["away_games"], 1)

    # 🔥 ELO dynamique
    elo = 1000 + (ppg * 120) + (form * 20)

    rows.append({
        "Team": team,
        "GoalsScoredAvg": round(goals_avg, 2),
        "GoalsConcededAvg": round(conceded_avg, 2),
        "PPG": round(ppg, 2),
        "Form": round(form, 2),
        "HomeAttack": round(home_attack, 2),
        "AwayAttack": round(away_attack, 2),
        "ELO": round(elo, 0)
    })

pd.DataFrame(rows).to_csv("data_processed/team_stats.csv", index=False)

print("✅ New advanced dataset ready")