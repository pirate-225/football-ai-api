import pandas as pd
from api.get_standings import get_standings

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

seasons = [2025]

all_standings = []

for season in seasons:
    for league_id, league_name in leagues.items():
        print(f"Downloading standings {league_name}...")
        df = get_standings(league_id, season)

        if df.empty:
            continue

        df["league_id"] = league_id
        df["league_name"] = league_name
        df["season"] = season

        all_standings.append(df)

if len(all_standings) > 0:
    final_standings = pd.concat(all_standings)
    final_standings.to_csv("data_raw/api_standings.csv", index=False)
    print("Standings downloaded successfully")
else:
    print("No standings downloaded")