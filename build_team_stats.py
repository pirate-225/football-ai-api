import pandas as pd
import os

print("Building team stats...")

matches = pd.read_csv("data_processed/master_dataset.csv")

# garder saisons récentes
matches = matches[matches["season"].isin([2024, 2025])]

matches = matches.sort_values("date")

teams = pd.unique(matches[["HomeTeam", "AwayTeam"]].values.ravel())

# 🔥 ELO INIT
elo = {team: 1500 for team in teams}
K = 20

stats = []

for team in teams:

    team_matches_home = matches[matches["HomeTeam"] == team]
    team_matches_away = matches[matches["AwayTeam"] == team]

    all_matches = pd.concat([team_matches_home, team_matches_away]).sort_values("date")

    if len(all_matches) < 10:
        continue

    # ---------- FORM ----------
    last5 = all_matches.tail(5)
    last10 = all_matches.tail(10)

    def compute_form(df):
        pts = 0
        for _, m in df.iterrows():
            if m["HomeTeam"] == team:
                if m["FTHG"] > m["FTAG"]:
                    pts += 3
                elif m["FTHG"] == m["FTAG"]:
                    pts += 1
            else:
                if m["FTAG"] > m["FTHG"]:
                    pts += 3
                elif m["FTAG"] == m["FTHG"]:
                    pts += 1
        return pts

    form5 = compute_form(last5) / 15
    form10 = compute_form(last10) / 30
    form = form5 * 0.7 + form10 * 0.3

    # ---------- GOALS ----------
    goals_scored = 0
    goals_conceded = 0
    clean_sheets = 0
    failed_score = 0

    for _, m in last10.iterrows():
        if m["HomeTeam"] == team:
            scored = m["FTHG"]
            conceded = m["FTAG"]
        else:
            scored = m["FTAG"]
            conceded = m["FTHG"]

        goals_scored += scored
        goals_conceded += conceded

        if conceded == 0:
            clean_sheets += 1
        if scored == 0:
            failed_score += 1

    gs_avg = goals_scored / len(last10)
    gc_avg = goals_conceded / len(last10)

    clean_rate = clean_sheets / len(last10)
    fail_rate = failed_score / len(last10)

    # ---------- PPG ----------
    total_points = 0
    home_points = 0
    away_points = 0

    for _, m in all_matches.iterrows():
        if m["HomeTeam"] == team:
            if m["FTHG"] > m["FTAG"]:
                total_points += 3
                home_points += 3
            elif m["FTHG"] == m["FTAG"]:
                total_points += 1
                home_points += 1
        else:
            if m["FTAG"] > m["FTHG"]:
                total_points += 3
                away_points += 3
            elif m["FTAG"] == m["FTHG"]:
                total_points += 1
                away_points += 1

    total_matches = len(all_matches)
    home_matches = len(team_matches_home)
    away_matches = len(team_matches_away)

    ppg = total_points / total_matches
    home_ppg = home_points / home_matches if home_matches > 0 else 0
    away_ppg = away_points / away_matches if away_matches > 0 else 0

    # ---------- ELO ----------
    team_elo = elo[team]

    stats.append({
        "Team": team,
        "PPG": ppg,
        "HomePPG": home_ppg,
        "AwayPPG": away_ppg,
        "Form": form,
        "GoalsScoredAvg": gs_avg,
        "GoalsConcededAvg": gc_avg,
        "CleanSheetRate": clean_rate,
        "FailToScoreRate": fail_rate,
        "MatchesPlayed": total_matches,
        "ELO": team_elo
    })

df = pd.DataFrame(stats)

os.makedirs("data_processed", exist_ok=True)
df.to_csv("data_processed/team_stats.csv", index=False)

print("team_stats.csv created")