import requests
import pandas as pd
import numpy as np
from fantasy import Fantasy
from tqdm import tqdm

url = "https://sports.core.api.espn.com/v3/sports/football/nfl/athletes?limit=18000"

print("Retrieving raw data from ESPN...")
jsonData = requests.get(url).json()

print("Creating dataframe...")
players = pd.DataFrame(jsonData['items'])

# Columns in 'players'
# ['id', 'uid', 'guid', 'lastName', 'fullName', 'displayName', 'shortName', 'jersey', 'active', 'firstName', 'weight', 'displayWeight', 'height', 'displayHeight', 'age', 'dateOfBirth', 'experience', 'birthPlace', 'dateOfDeath', 'hand', 'middleName', 'citizenship', 'nickname']

print("Players shape:", players.shape)

# Remove rows where 'active' is 'False'
print("Removing inactive players...")
players = players[players['active'] == True]

# write the dataframe to a csv file
print("Writing dataframe to csv...")
players.to_csv("players.csv")

print("Players shape:", players.shape)

# Remove all columns except for 'lastName', 'firstName', 'fullName'
print("Removing unnecessary columns...")
players = players[['lastName', 'firstName', 'fullName']]

# Create instance of Fantasy class
print("Creating instance of Fantasy class...")
fantasy = Fantasy()

# Get all player objects
player_objects = []
print("Gathering player objects...")
for i in tqdm(range(players.shape[0]), desc="Processing players"):
    # get player's full name
    try:
        player = fantasy.league.player_info(players.iloc[i]['fullName'])
    except:
        player = None

    # check if the player is NoneType
    if player is None:
        continue

    # add player's stats to list
    player_objects.append(player)

# Initilize dataframe
player_stats_df = pd.DataFrame(columns=['fullName', 'position', 'points'])

print("Creating dataframe of player stats...")
for object in tqdm(player_objects, desc="Creating dataframe of player stats"):
    
    # get player's name and position
    name = object.name
    position = object.position

    # create row for player
    player_row = {'fullName': name, 'position': position}

    # add player's stats to row
    for week in object.stats:
        for stat in object.stats[week]['breakdown']:
            
            # if the stat name is a digit or if the stat name starts with 'defensive', skip it
            if stat.isdigit() or stat.startswith('defensive'):
                continue

            # make the column name
            column_name = str(week) + '_' + stat
            
            # add column to row
            player_row[column_name] = object.stats[week]['breakdown'][stat]

    # add player's points to row
    player_row['points'] = object.stats[week]['points']

    # add row to dataframe
    player_stats_df = player_stats_df._append(player_row, ignore_index=True)


# check if any duplicate columns exist
print("Checking for duplicate columns...")
duplicates = 0
for column in player_stats_df.columns:
    if player_stats_df.columns.tolist().count(column) > 1:
        print("Duplicate column:", column)
        duplicates += 1

if duplicates == 0:
    print("No duplicate columns found")

# fill empty cells with NaN
print("Filling empty cells with NaN...")
player_stats_df = player_stats_df.fillna(value=np.nan)

# get first three columns: 'fullName', 'position', 'points'
meta_df = player_stats_df.iloc[:, :3]

# get all columns except for 'fullName', 'position', 'points'
stats_df = player_stats_df.iloc[:, 3:]

# Reorder the columns of stats_df in ascending order by the number at the beginning of the column name
# stats_df.reindex(sorted(stats_df.columns), axis=1) will sort it as a string, not as a number so 
# it will sort as 0, 10, 11, 12, 13, 14, 1, ..., 9. To fix this, we need to sort it as a number.
print("Sorting columns...")
stats_df = stats_df.reindex(sorted(stats_df.columns, key=lambda x: int(x.split('_')[0])), axis=1)

# Combine meta_df and stats_df
player_stats_df = pd.concat([meta_df, stats_df], axis=1)

# remove empty columns
print("Removing empty columns...")
player_stats_df = player_stats_df.dropna(axis=1, how='all')

# print the shape of the dataframe
print("Shape of dataframe:", player_stats_df.shape)

# write the dataframe to a csv file
print("Writing dataframe to csv...")
player_stats_df.to_csv("player_stats.csv")

# Split the dataset by position
print("Splitting dataset by position...")
datasets = player_stats_df.groupby('position')

# Create a dataframe for each position
print("Creating dataframe for each position...")
qb_df = datasets.get_group('QB')
rb_df = datasets.get_group('RB')
wr_df = datasets.get_group('WR')
te_df = datasets.get_group('TE')
k_df = datasets.get_group('K')

# drop the columns with 50% or more missing values
print("Removing columns with 50\% or more missing values...")
qb_df = qb_df.dropna(thresh=qb_df.shape[0] * 0.1, axis=1)
rb_df = rb_df.dropna(thresh=rb_df.shape[0] * 0.1, axis=1)
wr_df = wr_df.dropna(thresh=wr_df.shape[0] * 0.1, axis=1)
te_df = te_df.dropna(thresh=te_df.shape[0] * 0.1, axis=1)
k_df = k_df.dropna(thresh=k_df.shape[0] * 0.1, axis=1)

# drop the rows with 50% or more missing values
print("Removing rows with 50\% or more missing values...")
qb_df = qb_df.dropna(thresh=qb_df.shape[1] * 0.1, axis=0)
rb_df = rb_df.dropna(thresh=rb_df.shape[1] * 0.1, axis=0)
wr_df = wr_df.dropna(thresh=wr_df.shape[1] * 0.1, axis=0)
te_df = te_df.dropna(thresh=te_df.shape[1] * 0.1, axis=0)
k_df = k_df.dropna(thresh=k_df.shape[1] * 0.1, axis=0)

# write each dataframe to a csv file
print("Writing each dataframe to csv...")
qb_df.to_csv("qb_stats.csv")
rb_df.to_csv("rb_stats.csv")
wr_df.to_csv("wr_stats.csv")
te_df.to_csv("te_stats.csv")
k_df.to_csv("k_stats.csv")

print("Done!")