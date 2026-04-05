import pandas as pd
import os

# Charger features
df = pd.read_csv("data_processed/features.csv")

teams = {}

for index, row in df.iterrows():

    home_team = row['home_team']
    away_team = row['away_team']

    # Stats home team
    teams[home_team] = {
        'points_per_game': row['home_points_per_game'],
        'goals_scored_avg': row['home_goals_scored_avg'],
        'goals_conceded_avg': row['home_goals_conceded_avg'],
        'goal_diff': row['home_goal_diff_avg'],
        'over_ratio': row['home_over_ratio'],
        'btts_ratio': row['home_btts_ratio'],
        'form': row['home_form'],
        'elo': row['home_elo']
    }

    # Stats away team
    teams[away_team] = {
        'points_per_game': row['away_points_per_game'],
        'goals_scored_avg': row['away_goals_scored_avg'],
        'goals_conceded_avg': row['away_goals_conceded_avg'],
        'goal_diff': row['away_goal_diff_avg'],
        'over_ratio': row['away_over_ratio'],
        'btts_ratio': row['away_btts_ratio'],
        'form': row['away_form'],
        'elo': row['away_elo']
    }

# Convertir en DataFrame
team_rows = []

for team, stats in teams.items():
    team_rows.append([
        team,
        stats['points_per_game'],
        stats['goals_scored_avg'],
        stats['goals_conceded_avg'],
        stats['goal_diff'],
        stats['over_ratio'],
        stats['btts_ratio'],
        stats['form'],
        stats['elo']
    ])

team_df = pd.DataFrame(team_rows, columns=[
    'team',
    'points_per_game',
    'goals_scored_avg',
    'goals_conceded_avg',
    'goal_diff',
    'over_ratio',
    'btts_ratio',
    'form',
    'elo'
])

os.makedirs("data_processed", exist_ok=True)
team_df.to_csv("data_processed/team_stats.csv", index=False)

print("team_stats.csv créé !")