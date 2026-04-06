import pandas as pd

print("Loading matches...")
matches = pd.read_csv("data_processed/master_dataset.csv")

teams = pd.concat([matches["HomeTeam"], matches["AwayTeam"]]).unique()

team_stats = []

for team in teams:
    home_matches = matches[matches["HomeTeam"] == team]
    away_matches = matches[matches["AwayTeam"] == team]

    played = len(home_matches) + len(away_matches)
    if played == 0:
        continue

    # Goals scored / conceded
    goals_scored = home_matches["FTHG"].sum() + away_matches["FTAG"].sum()
    goals_conceded = home_matches["FTAG"].sum() + away_matches["FTHG"].sum()

    # Points
    points = 0
    for _, row in home_matches.iterrows():
        if row["FTHG"] > row["FTAG"]:
            points += 3
        elif row["FTHG"] == row["FTAG"]:
            points += 1

    for _, row in away_matches.iterrows():
        if row["FTAG"] > row["FTHG"]:
            points += 3
        elif row["FTAG"] == row["FTHG"]:
            points += 1

    points_per_game = points / played
    goal_diff = (goals_scored - goals_conceded) / played

    # Form last 5 matches
    last_matches = pd.concat([home_matches, away_matches]).sort_values("date").tail(5)
    form_points = 0

    for _, row in last_matches.iterrows():
        if row["HomeTeam"] == team:
            if row["FTHG"] > row["FTAG"]:
                form_points += 3
            elif row["FTHG"] == row["FTAG"]:
                form_points += 1
        else:
            if row["FTAG"] > row["FTHG"]:
                form_points += 3
            elif row["FTAG"] == row["FTHG"]:
                form_points += 1

    form = form_points / 5

    # Elo
    elo_home = home_matches["elo_home"].mean() if "elo_home" in home_matches else 1500
    elo_away = away_matches["elo_away"].mean() if "elo_away" in away_matches else 1500
    elo = (elo_home + elo_away) / 2

    # Position (approx via points)
    position_points = points

    team_stats.append([
        team,
        points_per_game,
        goal_diff,
        form,
        elo,
        position_points
    ])

team_stats_df = pd.DataFrame(team_stats, columns=[
    "Team",
    "PointsPerGame",
    "GoalDiff",
    "Form",
    "Elo",
    "Points"
])

# Position based on points
team_stats_df = team_stats_df.sort_values("Points", ascending=False)
team_stats_df["Position"] = range(1, len(team_stats_df) + 1)

team_stats_df.to_csv("data_processed/team_stats.csv", index=False)

print("team_stats.csv created")