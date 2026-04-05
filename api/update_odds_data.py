import pandas as pd
from api.get_odds import get_odds

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

season = 2024

all_odds = []

for league_id, league_name in leagues.items():
    print(f"Downloading odds {league_name}...")
    df = get_odds(league_id, season)

    if df.empty:
        continue

    df["league_id"] = league_id
    df["league_name"] = league_name

    all_odds.append(df)

if len(all_odds) > 0:
    final_odds = pd.concat(all_odds)
    final_odds.to_csv("data_raw/api_odds.csv", index=False)
    print("Odds downloaded successfully")
else:
    print("No odds downloaded")