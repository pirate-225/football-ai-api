import pandas as pd
import os

folder = "data"
files = os.listdir(folder)

dataframes = []

for file in files:
    if file.endswith(".csv"):
        print("Lecture :", file)
        df = pd.read_csv(os.path.join(folder, file))
        dataframes.append(df)

data = pd.concat(dataframes)
data = data.sort_values("Date")

data["Over25"] = (data["FTHG"] + data["FTAG"] >= 3).astype(int)
data["BTTS"] = ((data["FTHG"] > 0) & (data["FTAG"] > 0)).astype(int)
data["Result"] = data["FTR"].map({"H": 2, "D": 1, "A": 0})

data = data[[
    "HomeTeam","AwayTeam",
    "FTHG","FTAG",
    "B365H","B365D","B365A",
    "HS","AS","HST","AST","HC","AC",
    "Over25","BTTS","Result"
]]

data.to_csv("dataset.csv", index=False)

print("Dataset créé : dataset.csv")