import pandas as pd
from api.get_fixtures import get_fixtures

leagues = {
    39: "Premier_League",
    61: "Ligue_1",
    140: "La_Liga",
    135: "Serie_A",
    78: "Bundesliga",
    71: "Brazil",
    128: "Argentina",
    265: "Chile",
    239: "Colombia",
    98: "Japan",
    292: "Korea",
    188: "Australia"
}

seasons = [2025, 2024, 2023, 2022, 2021]

all_matches = []

for season in seasons:
    print(f"Season {season}")
    for league_id, league_name in leagues.items():
        print(f"Downloading {league_name} {season}...")
        df = get_fixtures(league_id, season)

        if df.empty:
            continue

        df["league_id"] = league_id
        df["league_name"] = league_name
        df["season"] = season

        all_matches.append(df)

if len(all_matches) > 0:
    final_df = pd.concat(all_matches)
    final_df.to_csv("data_raw/api_matches_all_leagues.csv", index=False)
    print("All leagues and seasons downloaded successfully")
else:
    print("No matches downloaded")