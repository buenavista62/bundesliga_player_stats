import pandas as pd


# Define the Player parent class
class Player:
    def __init__(self, row):
        self.id = row["id"]  # Player ID
        self.player = row["Player"]  # Player Name
        self.nation = row["Nation"]  # Nationality
        self.pos = row["Pos"]  # Position
        self.squad = row["Squad"]  # Squad
        self.age = row["Age"]  # Age
        self.born = row["Born"]  # Born
        self.matches_played = row["MP"]  # Matches Played
        self.starts = row["Starts"]  # Starts
        self.minutes = row["Min"]  # Minutes Played
        self.goals = row["Gls"]  # Goals
        self.assists = row["Ast"]  # Assists
        self.yellow_card = row["CrdY"]  # Yellow Cards
        self.red_card = row["CrdR"]  # Red Cards
        self.xG = row["xG"]  # Expected Goals
        self.npxG = row["npxG"]  # Non-Penalty Expected Goals
        self.xAG = row["xAG"]  # Expected Assists
        self.PrgC = row["PrgC"]  # Progressive Carries
        self.PrgP = row["PrgP"]  # Progressive Passes
        self.PrgR = row["PrgR"]  # Progressive Receptions

    def __str__(self):
        return f"{self.player} ({self.nation}) - {self.pos} - Age: {self.age}"


# Define the Striker sub-class
class Striker(Player):
    def __init__(self, row):
        super().__init__(row)
        self.shots = row["Sh"]  # Shots
        self.shots_on_target = row["SoT"]  # Shots on Target
        self.shots_on_target_pct = row["SoT%"]  # Shots on Target %
        self.goals_per_shot_on_target = row["G/SoT"]  # Goals per Shot on Target
        self.goals_per_shot = row["G/Sh"]  # Goals per Shot

    def __str__(self):
        return f"{super().__str__()} - Goals: {self.goals} - Shots: {self.shots}"


# Define the Midfielder sub-class
class Midfielder(Player):
    def __init__(self, row):
        super().__init__(row)
        self.passes_completed = row["Cmp"]  # Passes Completed
        self.passed_attempted = row["Att"]  # Passes Attempted
        self.passes_completed_pct = row["Cmp%"]  # Passes Completed %
        self.total_passing_distance = row["TotDist"]
        self.progressive_passing_distance = row[
            "PrgDist"
        ]  # Progressive Passing Distance
        self.key_passes = row["KP"]  # Key Passes
        self.final_third_passes = row["1/3"]  # Final Third Passes
        self.passes_into_penalty_area = row["PPA"]  # Passes into Penalty Area
        self.crosses_into_penalty_area = row["CrsPA"]  # Crosses into Penalty Area

    def __str__(self):
        return f"{super().__str__()} - Passes: {self.passes} - Tackles: {self.tackles}"


# Define the Defender sub-class
class Defender(Player):
    def __init__(self, row):
        super().__init__(row)
        self.tackles = row["Tkl"]  # Tackles
        self.attempts = row["Att"]  # Tackles Attempted
        self.tackles_pct = row["Tkl%"]  # Tackles %
        self.challenges_lost = row["Lost"]  # Challenges Lost
        self.blocks = row["Blocks"]  # Blocks
        self.shots_blocked = row["Sh"]  # shots Blocks
        self.passes_blocked = row["Pass"]  # Passes Blocked
        self.interceptions = row["Int"]  # Interceptions
        self.clears = row["Clr"]  # Clears
        self.errors = row["Err"]  # Errors

    def __str__(self):
        return f"{super().__str__()} - Tackles: {self.tackles} - Interceptions: {self.interceptions}"


# Define the Goalkeeper sub-class
class Goalkeeper(Player):
    def __init__(self, row):
        super().__init__(row)
        self.goals_against = row["GA"]  # Goals Against
        self.shots_on_target_against = row["SoTA"]  # Shots on Target Against
        self.saves = row["Saves"]  # Saves
        self.save_pct = row["Save%"]  # Save %
        self.clean_sheets = row["CS"]  # Clean Sheets
        self.clean_sheets_pct = row["CS%"]  # Clean Sheets %
        self.penalty_kicks_against = row["PKA"]  # Penalty Kicks Against
        self.penalty_kicks_saved = row["PKsv"]  # Penalty Kicks Saved
        self.penalty_kicks_missed = row["PKm"]  # Penalty Kicks Missed

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

# remove G+A G-PK and xnxG+xAG columns
df = df.loc[:, ~df.columns.str.startswith(("G+A", "G-PK", "xG+xA"))]

# extend data by goalkeeper data
df_gk = pd.read_csv("data/bundesliga_gk_stats.csv")

# remove all redundant columns
df_gk = df_gk.loc[:, ~df_gk.columns.str.startswith(("Playing", "-additional"))]
df_gk = df_gk.iloc[:, 1:-2]

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

# remove all columns ending with _y
df_gk = df_gk.loc[:, ~df_gk.columns.str.endswith("_y")]

# id on first column
fc = df_gk.pop("id")
df_gk.insert(0, "id", fc)

# remove column name suffix
df_gk.columns = df_gk.columns.str.replace("_x", "")

# match id, midfielder
df_mf = df_mf.merge(df, on=["Player", "Nation", "Pos", "Age"], how="inner")

# remove all columns ending with _y
df_mf = df_mf.loc[:, ~df_mf.columns.str.endswith("_y")]

# id on first column
fc = df_mf.pop("id")
df_mf.insert(0, "id", fc)

# remove suffix
df_mf.columns = df_mf.columns.str.replace("_x", "")

# match id, defender
df_df = df_df.merge(df, on=["Player", "Nation", "Pos", "Age"], how="inner")

# remove all columns ending with _y
df_df = df_df.loc[:, ~df_df.columns.str.endswith("_y")]

# id on first column
fc = df_df.pop("id")
df_df.insert(0, "id", fc)

# remove suffix
df_df.columns = df_df.columns.str.replace("_x", "")

# match id, forward
df_fw = df_fw.merge(df, on=["Player", "Nation", "Pos", "Age"], how="inner")

# remove all columns ending with _y
df_fw = df_fw.loc[:, ~df_fw.columns.str.endswith("_y")]

# id on first column
fc = df_fw.pop("id")
df_fw.insert(0, "id", fc)

# remove suffix
df_fw.columns = df_fw.columns.str.replace("_x", "")

# remove per 90 columns
df_gk = df_gk.loc[:, ~df_gk.columns.str.endswith("90")]
df_mf = df_mf.loc[:, ~df_mf.columns.str.endswith("90")]
df_df = df_df.loc[:, ~df_df.columns.str.endswith("90")]
df_fw = df_fw.loc[:, ~df_fw.columns.str.endswith("90")]

# remove W D and L columns from df_gk
df_gk = df_gk.loc[:, ~df_gk.columns.str.startswith("W")]
df_gk = df_gk.loc[:, ~df_gk.columns.str.startswith("D")]
df_gk = df_gk.loc[:, ~df_gk.columns.str.startswith("L")]

# remove pkatt from df_gk
df_gk = df_gk.loc[:, ~df_gk.columns.str.startswith("PKatt")]


# create instances of each subclass
gk_instances = []
for index, row in df_gk.iterrows():
    gk = Goalkeeper(row)
    gk_instances.append(gk)

mf_instances = []
for index, row in df_mf.iterrows():
    mf = Midfielder(row)
    mf_instances.append(mf)

df_instances = []
for index, row in df_df.iterrows():
    df = Defender(row)
    df_instances.append(df)

fw_instances = []
for index, row in df_fw.iterrows():
    fw = Striker(row)
    fw_instances.append(fw)

# create a list of all players
players = gk_instances + mf_instances + df_instances + fw_instances
