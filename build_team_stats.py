import pandas as pd

print("Lecture des matchs API...")

matches = pd.read_csv("data_raw/api_matches_all_leagues.csv")

# Renommer colonnes
matches = matches.rename(columns={
    "date": "Date",
    "home_team": "HomeTeam",
    "away_team": "AwayTeam",
    "home_goals": "FTHG",
    "away_goals": "FTAG"
})

teams = pd.concat([matches["HomeTeam"], matches["AwayTeam"]]).unique()

team_stats = []

for team in teams:
    home_matches = matches[matches["HomeTeam"] == team]
    away_matches = matches[matches["AwayTeam"] == team]

    goals_scored = home_matches["FTHG"].sum() + away_matches["FTAG"].sum()
    goals_conceded = home_matches["FTAG"].sum() + away_matches["FTHG"].sum()

    matches_played = len(home_matches) + len(away_matches)

    if matches_played == 0:
        continue

    team_stats.append({
        "Team": team,
        "Matches": matches_played,
        "GoalsScoredAvg": goals_scored / matches_played,
        "GoalsConcededAvg": goals_conceded / matches_played,
        "GoalDiffAvg": (goals_scored - goals_conceded) / matches_played
    })

team_stats_df = pd.DataFrame(team_stats)

team_stats_df.to_csv("data_processed/team_stats.csv", index=False)

print("team_stats.csv créé !")