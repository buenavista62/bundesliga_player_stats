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
        Gls,
        sh,
        Sot,
        SoTPCT,
        GperShot,
        Dist,
        FK,
        PK,
        PKatt,
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
        self.goals = goals
        self.shots = sh
        self.shots_on_target = Sot
        self.shots_on_target_pct = SoTPCT
        self.goals_per_shot = GperShot
        self.distance = Dist
        self.free_kicks = FK
        self.penalties = PK
        self.penalties_attempted = PKatt

    def __str__(self):
        return f"{super().__str__()} - Goals: {self.goals} - Shots: {self.shots}"


# Define the Midfielder sub-class
class Midfielder(Player):
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
        cmp,
        att,
        totdist,
        prgdist,
        kp,
        finalthird,
        ppa,
        crspa,
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
        self.passes_completed = cmp
        self.passed_attempted = att
        self.total_passing_distance = totdist
        self.progressive_passing_distance = prgdist
        self.key_passes = kp
        self.final_third_passes = finalthird
        self.passes_into_penalty_area = ppa
        self.crosses_into_penalty_area = crspa

    def __str__(self):
        return f"{super().__str__()} - Passes: {self.passes} - Tackles: {self.tackles}"


# Define the Defender sub-class
class Defender(Player):
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
        tackles,
        attempts,
        shots_blocked,
        passes_blocked,
        interceptions,
        clears,
        errors,
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
        self.tackles = tackles
        self.attempts = attempts
        self.shots_blocked = shots_blocked
        self.passes_blocked = passes_blocked
        self.interceptions = interceptions
        self.clears = clears
        self.errors = errors

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

# remove PK and Pkatt columns
df = df.loc[:, ~df.columns.str.startswith(("PK", "Pkatt"))]

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

# remove the first column
df_mf = df_mf.iloc[:, 1:]


# extend data by defensive stats (for defender)
df_df = pd.read_csv("data/bundesliga_df_stats.csv")

# remove all columns starting with tackles
df_df = df_df.loc[:, ~df_df.columns.str.startswith("Tackles")]
df_df = df_df.iloc[:, 1:-2]

# first row should be column
df_df.columns = df_df.iloc[0]
df_df = df_df.iloc[1:, :]

# clean-up columns nation, pos, age
df_df["Nation"] = df_df["Nation"].str[-3:]
df_df["Pos"] = df_df["Pos"].str[:2]
df_df["Age"] = pd.to_numeric(df_df["Age"].str[:2])


# select only defender
df_df = df_df.loc[df_df["Pos"] == "DF", :]

# remove tkl+int column
df_df = df_df.drop("Tkl+Int", axis=1)

# extend data by attacking stats (for forward)
df_fw = pd.read_csv("data/bundesliga_fw_stats.csv")

# remove all columns starting with expected
df_fw = df_fw.loc[:, ~df_fw.columns.str.startswith("Expected")]

# first row should be column
df_fw.columns = df_fw.iloc[0]
df_fw = df_fw.iloc[1:, :]

# clean-up columns nation, pos, age
df_fw["Nation"] = df_fw["Nation"].str[-3:]
df_fw["Pos"] = df_fw["Pos"].str[:2]
df_fw["Age"] = pd.to_numeric(df_fw["Age"].str[:2])

# select only forward
df_fw = df_fw.loc[df_fw["Pos"] == "FW", :]

# remove the last 2 columns and the first column
df_fw = df_fw.iloc[:, 1:-2]

# create a column id for each player
df["id"] = df.index
fc = df.pop("id")
df.insert(0, "id", fc)

# check if length of players dataframe is the same as the sum of the other dataframes
print(len(df))
print(len(df_gk) + len(df_mf) + len(df_df) + len(df_fw))

# match id of players dataframe with the other dataframes by player name, nation and position
df_gk = df_gk.merge(df, on=["Player", "Nation", "Pos", "Age"], how="inner")
df_gk = df_gk.loc[:, :"id"]

fc = df_gk.pop("id")
df_gk.insert(0, "id", fc)

# remove column name suffix
df_gk.columns = df_gk.columns.str.replace("_x", "")


df_mf = df_mf.merge(df, on=["Player", "Nation", "Pos", "Age"], how="inner")
df_mf = df_mf.loc[:, :"id"]

fc = df_mf.pop("id")
df_mf.insert(0, "id", fc)

# remove suffix
df_mf.columns = df_mf.columns.str.replace("_x", "")

df_df = df_df.merge(df, on=["Player", "Nation", "Pos", "Age"], how="inner")
df_df = df_df.loc[:, :"id"]

fc = df_df.pop("id")
df_df.insert(0, "id", fc)

# remove suffix
df_df.columns = df_df.columns.str.replace("_x", "")

df_fw = df_fw.merge(df, on=["Player", "Nation", "Pos", "Age"], how="inner")
df_fw = df_fw.loc[:, :"id"]

fc = df_fw.pop("id")
df_fw.insert(0, "id", fc)

# remove suffix
df_fw.columns = df_fw.columns.str.replace("_x", "")
