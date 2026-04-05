import pandas as pd
from api.get_fixtures import get_fixtures

leagues = {
    39: "Premier_League",
    40: "Championship",
    61: "Ligue_1",
    62: "Ligue_2",
    140: "La_Liga",
    141: "La_Liga_2",
    135: "Serie_A",
    136: "Serie_B",
    78: "Bundesliga",
    79: "Bundesliga_2",
    88: "Eredivisie",
    94: "Portugal",
    144: "Belgium",
    203: "Turkey",
    71: "Brazil_A",
    72: "Brazil_B",
    128: "Argentina",
    265: "Chile",
    239: "Colombia",
    268: "Uruguay",
    281: "Peru",
    98: "Japan",
    292: "Korea",
    188: "Australia"
}

season = 2024

all_matches = []

for league_id, league_name in leagues.items():
    print(f"Downloading {league_name}...")
    try:
        df = get_fixtures(league_id, season)
        df["league_id"] = league_id
        df["league_name"] = league_name
        all_matches.append(df)
    except Exception as e:
        print(f"Error with {league_name}: {e}")

final_df = pd.concat(all_matches)
final_df.to_csv("data_raw/api_matches_all_leagues.csv", index=False)

print("All leagues downloaded successfully")