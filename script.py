import requests
from bs4 import BeautifulSoup
import pandas as pd


# Define the Player parent class
class Player:
    def __init__(
        self,
        name,
        nationality,
        position,
        squad,
        age,
        born,
        matches_played,
        starts,
        minutes,
        goals,
        assists,
        yellow_card,
        red_card,
        xG,
        npxG,
        xAG,
        PrgC,
        PrgP,
        PrgR,
    ):
        self.name = name
        self.position = position
        self.age = age
        self.nationality = nationality
        self.squad = squad
        self.born = born
        self.matches_played = matches_played
        self.started = starts
        self.minutes = minutes
        self.goals = goals
        self.assists = assists
        self.ycards = yellow_card
        self.rcards = red_card
        self.xG = xG
        self.npxG = npxG
        self.xAG = xAG
        self.PrgC = PrgC
        self.PrgP = PrgP
        self.PrgR = PrgR

    def __str__(self):
        return f"{self.name} ({self.nationality}) - {self.position} - Age: {self.age}"


# Define the Striker sub-class
class Striker(Player):
    def __init__(self, name, position, age, nationality, goals, shots):
        super().__init__(name, position, age, nationality)
        self.goals = goals
        self.shots = shots

    def __str__(self):
        return f"{super().__str__()} - Goals: {self.goals} - Shots: {self.shots}"


# Define the Midfielder sub-class
class Midfielder(Player):
    def __init__(self, name, position, age, nationality, passes, tackles):
        super().__init__(name, position, age, nationality)
        self.passes = passes
        self.tackles = tackles

    def __str__(self):
        return f"{super().__str__()} - Passes: {self.passes} - Tackles: {self.tackles}"


# Define the Defender sub-class
class Defender(Player):
    def __init__(self, name, position, age, nationality, tackles, interceptions):
        super().__init__(name, position, age, nationality)
        self.tackles = tackles
        self.interceptions = interceptions

    def __str__(self):
        return f"{super().__str__()} - Tackles: {self.tackles} - Interceptions: {self.interceptions}"


# Define the Goalkeeper sub-class
class Goalkeeper(Player):
    def __init__(
        self,
        name,
        nationality,
        position,
        squad,
        age,
        born,
        matches_played,
        starts,
        minutes,
        goals,
        assists,
        yellow_card,
        red_card,
        xG,
        npxG,
        xAG,
        PrgC,
        PrgP,
        PrgR,
        GA,
        SoTA,
        Saves,
        CS,
        PKsv,
        PKm,
    ):
        super().__init__(
            self,
            name,
            nationality,
            position,
            squad,
            age,
            born,
            matches_played,
            starts,
            minutes,
            goals,
            assists,
            yellow_card,
            red_card,
            xG,
            npxG,
            xAG,
            PrgC,
            PrgP,
            PrgR,
        )
        self.saves = Saves
        self.clean_sheets = CS
        self.PK_saved = PKsv
        self.PK_missed = PKm

    def __str__(self):
        return f"{super().__str__()} - Saves: {self.saves} - Clean Sheets: {self.clean_sheets}"


df = pd.read_csv("data/bundesliga_player_stats.csv")

# remove all 'per90' columns
df = df.loc[:, ~df.columns.str.startswith("Per 90")]

# first row should be column
df.columns = df.iloc[0]
df = df.iloc[1:, :]

# remove first and last 2 columns
df = df.iloc[:, 1:-2]

# clean-up columns nation, pos, age
df["Nation"] = df["Nation"].str[-3:]
df["Pos"] = df["Pos"].str[:2]
df["Age"] = pd.to_numeric(df["Age"].str[:2])

# check type of columns
print(df.dtypes)

# change from object to numeric
num_cols = list(df.loc[:, "Born":].columns.values)
df[num_cols] = df[num_cols].apply(pd.to_numeric)

# extend data by goalkeeper data
df_gk = pd.read_csv("data/bundesliga_gk_stats.csv")

# remove all redundant columns
df_gk = df_gk.loc[:, ~df_gk.columns.str.startswith(("Playing", "-additional"))]
df_gk = df_gk.iloc[:, 1:-1]

# first row should be column
df_gk.columns = df_gk.iloc[0]
df_gk = df_gk.iloc[1:, :]

# clean-up columns nation, pos, age
df_gk["Nation"] = df_gk["Nation"].str[-3:]
df_gk["Pos"] = df_gk["Pos"].str[:2]
df_gk["Age"] = pd.to_numeric(df_gk["Age"].str[:2])

# extend data by passing stats (for midfielder)
df_mf = pd.read_csv("data/bundesliga_mf_stats.csv")
df_mf = df_mf.loc[
    :,
    ~df_mf.columns.str.startswith(
        (
            "Short",
            "Medium",
            "Long",
            "Unnamed: 23",
            "Unnamed: 24",
            "Unnamed: 25",
            "Unnamed: 31",
            "-add",
        )
    ),
]
df_mf.columns = df_mf.iloc[0]
df_mf = df_mf.iloc[1:, :]


# clean-up columns nation, pos, age
df_mf["Nation"] = df_mf["Nation"].str[-3:]
df_mf["Pos"] = df_mf["Pos"].str[:2]
df_mf["Age"] = pd.to_numeric(df_mf["Age"].str[:2])


# select only midfielder
df_mf = df_mf.loc[df_mf["Pos"] == "MF", :]

# generate a function to add two numbers
