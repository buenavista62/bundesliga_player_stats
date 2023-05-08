import pandas as pd
import matplotlib.pyplot as plt
import pandas_profiling as pp


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

    def get_club_players(players, team_name, position=None):
        if position == None:
            return [player.player for player in players if player.squad == team_name]
        elif position in ["DF", "MF", "FW", "GK"]:
            return [
                player.player
                for player in players
                if player.squad == team_name and player.pos == position
            ]
        else:
            return "Invalid Position"

    def team_analysis(players, team_name):
        team_players = Player.get_club_players(players, team_name)
        team_players.sort()
        print(f"Players in {team_name}: {team_players}")
        print(f"Total Players: {len(team_players)}")

        team_data = [
            players.__dict__ for players in players if players.squad == team_name
        ]
        team_data = pd.DataFrame.from_dict(team_data)

        print(f"Total Goals: {team_data['goals'].sum()}")
        print(f"Total Assists: {team_data['assists'].sum()}")
        print(f"Total Minutes Played: {team_data['minutes'].sum()}")
        print(f"Total Yellow Cards: {team_data['yellow_card'].sum()}")
        print(f"Total Red Cards: {team_data['red_card'].sum()}")
        print(f"Total Expected Goals: {team_data['xG'].sum()}")
        print(f"Total Non-Penalty Expected Goals: {team_data['npxG'].sum()}")

        team_data["goals_per_90"] = team_data["goals"] / (team_data["minutes"] / 90)
        team_data["assists_per_90"] = team_data["assists"] / (team_data["minutes"] / 90)
        team_data["goals_and_assists_per_90"] = (
            team_data["goals_per_90"] + team_data["assists_per_90"]
        )
        team_data["xG_per_90"] = team_data["xG"] / (team_data["minutes"] / 90)
        team_data["npxG_per_90"] = team_data["npxG"] / (team_data["minutes"] / 90)

        pp.ProfileReport(team_data)

        return team_data


Hoffenheim_team = Player.team_analysis(players, "Hoffenheim")


Player.team_analysis(players, "Hoffenheim")
Player.get_club_players(players, "Hoffenheim", "FW")


players[players["Squad"] == "Hoffenheim"]


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

    def goals_comparison(self, other):
        if self.goals > other.goals:
            return f"{self.player} is a better striker than {other.player}"
        elif self.goals < other.goals:
            return f"{other.player} is a better striker than {self.player}"
        else:
            return f"{self.player} and {other.player} are equally good strikers"

    def compare_with_others(self, players):
        xg_values = [player.xG for player in players]
        xag_values = [player.xAG for player in players]

        # create scatter plot of xG vs. xA for all players
        plt.scatter(xag_values, xg_values, c="b", marker="x", label="Other Players")

        # highlight the current player's position on the plot with a red marker
        current_player_index = players.index(self)
        plt.scatter(
            xag_values[current_player_index],
            xg_values[current_player_index],
            c="r",
            marker="o",
            label=self.player,
        )

        # add axis labels and title to the plot
        plt.xlabel("xAG")
        plt.ylabel("xG")
        plt.legend(loc="upper left")
        plt.grid(True)
        plt.title("Comparison of xG vs. xAG for all Strikers")

        plt.show()


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

    def compare_with_all(self, players):
        # Create two empty lists to store the names and difference of each player compared to the current player
        names = []
        differences = []

        # Iterate over all the players in the input list
        for player in players:
            # Check if the player is a Defender instance
            if isinstance(player, Defender):
                # Calculate the Difference between the current player and the player in the loop based on their tackles and interceptions
                difference = (
                    (self.tackles - player.tackles)
                    + (self.interceptions - player.interceptions)
                ) / 2
                # Add the player's name and difference to the corresponding lists
                names.append(player.player)
                differences.append(difference)

        # Print the results
        print(f"Comparison of {self.player} with all other Defenders:")
        for name, difference in zip(names, differences):
            print(f"{name}: {difference}")

        # Plot the results
        plt.bar(names, differences)
        plt.title(f"Comparison of {self.player} with all other Defenders")
        plt.xlabel("Player Name")
        plt.ylabel("difference")
        plt.xticks(rotation=90, fontsize=4)
        plt.show()


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

# change from object to numeric
num_cols = list(df_gk.loc[:, "Born":].columns.values)
df_gk[num_cols] = df_gk[num_cols].apply(pd.to_numeric)

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

# change from object to numeric
num_cols = list(df_mf.loc[:, "Born":].columns.values)
df_mf[num_cols] = df_mf[num_cols].apply(pd.to_numeric)

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

# change from object to numeric
num_cols = list(df_df.loc[:, "Born":].columns.values)
df_df[num_cols] = df_df[num_cols].apply(pd.to_numeric)

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

# change from object to numeric
num_cols = list(df_fw.loc[:, "Born":].columns.values)
df_fw[num_cols] = df_fw[num_cols].apply(pd.to_numeric)

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


fw_instances[60].compare_with_others(fw_instances)


abcd = [1, 5, 6, 8, 23, 3]
abcd[0:3] + abcd[4::]

df_instances[17].compare_with_all(df_instances)

df_instances[2].__dict__
fw_instances[8].__dict__

[player.player for player in players if player.squad == "Hoffenheim"]

oppp = [player.__dict__ for player in players if player.squad == "Hoffenheim"]

pd.DataFrame.from_dict(oppp)
