import pandas as pd

print("Loading matches...")
matches = pd.read_csv("data_raw/api_matches_all_leagues.csv")

matches = matches.sort_values("date")

teams = pd.concat([matches["home_team"], matches["away_team"]]).unique()

form_dict = {team: [] for team in teams}
form_home = []
form_away = []

for index, row in matches.iterrows():
    home = row["home_team"]
    away = row["away_team"]
    hg = row["home_goals"]
    ag = row["away_goals"]

    # Get last 5 results
    home_form = form_dict[home][-5:]
    away_form = form_dict[away][-5:]

    form_home.append(sum(home_form)/5 if len(home_form) == 5 else 1.5)
    form_away.append(sum(away_form)/5 if len(away_form) == 5 else 1.5)

    # Update results
    if hg > ag:
        form_dict[home].append(3)
        form_dict[away].append(0)
    elif hg < ag:
        form_dict[home].append(0)
        form_dict[away].append(3)
    else:
        form_dict[home].append(1)
        form_dict[away].append(1)

matches["home_form"] = form_home
matches["away_form"] = form_away

matches.to_csv("data_processed/matches_with_form.csv", index=False)

print("Form added")