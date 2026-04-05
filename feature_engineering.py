import pandas as pd
import glob
import os

# Lire tous les fichiers CSV
files = glob.glob("data_raw/*.csv")

df_list = []
for file in files:
    print("Lecture :", file)
    df = pd.read_csv(file, encoding='latin1')
    df_list.append(df)

matches = pd.concat(df_list, ignore_index=True)

# Convert date
matches['Date'] = pd.to_datetime(matches['Date'], dayfirst=True, errors='coerce')

# Trier par date
matches = matches.sort_values('Date')

teams = {}
elo_ratings = {}
rows = []

K = 20

def get_team(team):
    if team not in teams:
        teams[team] = {
            'matches': 0,
            'points': 0,
            'goals_scored': 0,
            'goals_conceded': 0,
            'over': 0,
            'btts': 0,
            'last_results': []
        }
    return teams[team]

def get_elo(team):
    if team not in elo_ratings:
        elo_ratings[team] = 1500
    return elo_ratings[team]

def update_elo(home, away, result):
    home_elo = elo_ratings[home]
    away_elo = elo_ratings[away]

    expected_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
    expected_away = 1 / (1 + 10 ** ((home_elo - away_elo) / 400))

    if result == 'H':
        score_home = 1
        score_away = 0
    elif result == 'D':
        score_home = 0.5
        score_away = 0.5
    else:
        score_home = 0
        score_away = 1

    elo_ratings[home] = home_elo + K * (score_home - expected_home)
    elo_ratings[away] = away_elo + K * (score_away - expected_away)

def compute_features(stats):
    if stats['matches'] == 0:
        return [0]*7

    points_per_game = stats['points'] / stats['matches']
    goals_scored_avg = stats['goals_scored'] / stats['matches']
    goals_conceded_avg = stats['goals_conceded'] / stats['matches']
    goal_diff_avg = (stats['goals_scored'] - stats['goals_conceded']) / stats['matches']
    over_ratio = stats['over'] / stats['matches']
    btts_ratio = stats['btts'] / stats['matches']

    last = stats['last_results'][-5:]
    form = sum(last) / (len(last)*3) if len(last) > 0 else 0

    return [
        points_per_game,
        goals_scored_avg,
        goals_conceded_avg,
        goal_diff_avg,
        over_ratio,
        btts_ratio,
        form
    ]

for index, match in matches.iterrows():

    if pd.isna(match['FTHG']) or pd.isna(match['FTAG']):
        continue

    home = match['HomeTeam']
    away = match['AwayTeam']
    home_goals = match['FTHG']
    away_goals = match['FTAG']
    result = match['FTR']

    odds_home = match.get('B365H', 0)
    odds_draw = match.get('B365D', 0)
    odds_away = match.get('B365A', 0)

    home_stats = get_team(home)
    away_stats = get_team(away)

    home_features = compute_features(home_stats)
    away_features = compute_features(away_stats)

    # ELO
    home_elo = get_elo(home)
    away_elo = get_elo(away)
    elo_diff = home_elo - away_elo

    # Diff features
    form_diff = home_features[6] - away_features[6]
    points_diff = home_features[0] - away_features[0]
    goal_diff_diff = home_features[3] - away_features[3]
    over_diff = home_features[4] - away_features[4]
    btts_diff = home_features[5] - away_features[5]

    odds_ratio = 0
    if odds_away != 0:
        odds_ratio = odds_home / odds_away

    over25 = 1 if home_goals + away_goals > 2 else 0
    btts = 1 if home_goals > 0 and away_goals > 0 else 0

    rows.append([
        home,
        away,
        *home_features,
        *away_features,
        form_diff,
        points_diff,
        goal_diff_diff,
        over_diff,
        btts_diff,
        odds_ratio,
        home_elo,
        away_elo,
        elo_diff,
        odds_home,
        odds_draw,
        odds_away,
        result,
        over25,
        btts
    ])

    # Update stats
    home_stats['matches'] += 1
    away_stats['matches'] += 1

    home_stats['goals_scored'] += home_goals
    home_stats['goals_conceded'] += away_goals

    away_stats['goals_scored'] += away_goals
    away_stats['goals_conceded'] += home_goals

    if result == 'H':
        home_stats['points'] += 3
        home_stats['last_results'].append(3)
        away_stats['last_results'].append(0)
    elif result == 'D':
        home_stats['points'] += 1
        away_stats['points'] += 1
        home_stats['last_results'].append(1)
        away_stats['last_results'].append(1)
    else:
        away_stats['points'] += 3
        home_stats['last_results'].append(0)
        away_stats['last_results'].append(3)

    if over25:
        home_stats['over'] += 1
        away_stats['over'] += 1

    if btts:
        home_stats['btts'] += 1
        away_stats['btts'] += 1

    # Update ELO
    update_elo(home, away, result)

columns = [
    'home_team',
    'away_team',

    'home_points_per_game',
    'home_goals_scored_avg',
    'home_goals_conceded_avg',
    'home_goal_diff_avg',
    'home_over_ratio',
    'home_btts_ratio',
    'home_form',

    'away_points_per_game',
    'away_goals_scored_avg',
    'away_goals_conceded_avg',
    'away_goal_diff_avg',
    'away_over_ratio',
    'away_btts_ratio',
    'away_form',

    'form_diff',
    'points_diff',
    'goal_diff_diff',
    'over_diff',
    'btts_diff',
    'odds_ratio',

    'home_elo',
    'away_elo',
    'elo_diff',

    'odds_home',
    'odds_draw',
    'odds_away',

    'result',
    'over25',
    'btts'
]

features_df = pd.DataFrame(rows, columns=columns)

os.makedirs("data_processed", exist_ok=True)
features_df.to_csv("data_processed/features.csv", index=False)

print("features.csv FINAL créé !")