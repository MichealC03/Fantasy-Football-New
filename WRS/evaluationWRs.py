import pandas as pd
from sleeper import sleeperDf
from underdog import underDogDf

# init variables
PassingMult = .04
RushingMult = .1
ReceivingMult = .1
PassingTd = 6
RushingTd = 10
Interceptions = -2
Fumbles = -2
RBPPR = .5
WRPPR = 1
TEPPR = 1.5


def renameDf(df):
    # Adjustments for predictions
    if 'G' not in df.columns:
        df['G'] = 17

    if 'TD' not in df.columns:
        df.rename(columns={
        'TDS': 'TD',
        'TDS.1': 'TD.1',
    }, inplace=True)

    df = df[['Player','YDS', 'TD', 'REC', 'YDS.1', 'TD.1', 'G', 'FPTS', 'FL']]

    df.rename(columns={
        'Player': 'Name',
        'YDS': 'Receiving_Yards',
        'TD': 'Receiving_Touchdowns',
        'REC': 'Receptions',
        'YDS.1': 'Rushing_Yards',
        'TD.1': 'Rushing_Touchdowns',
        'G': 'Games_Played',
        'FPTS': 'Fantasy_Points',
        'FL': 'Fumbles'
    }, inplace=True)

    return df

def convertCols(df):
    # Convert relevant columns to numeric types
    numeric_columns = [
        'Rushing_Yards',
        'Rushing_Touchdowns',
        'Receptions',
        'Receiving_Yards',
        'Receiving_Touchdowns',
        'Games_Played',
        'Fantasy_Points',
        'Fumbles'
    ]

    for col in numeric_columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].str.replace(',', '', regex=False)  # Remove commas
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric

    return df

def newTotal(df):
    # Calculate the new Fantasy Points based on the multipliers
    df['Adjusted_Fantasy_Points'] = (
        df['Receiving_Yards'] * ReceivingMult +
        df['Receiving_Touchdowns'] * PassingTd +
        df['Rushing_Yards'] * RushingMult +
        df['Rushing_Touchdowns'] * RushingTd +
        df['Fumbles'] * Fumbles +
        df['Receptions'] * WRPPR
    )

    return df

def getPointsPerGame(df):
    # Create a new column of pts per game
    df['PTS/P/G'] = df['Adjusted_Fantasy_Points'] / df['Games_Played']

    # sort by pts per game

    df_sorted = df.sort_values(by='PTS/P/G', ascending=False)

    return df_sorted.reset_index(drop=True)[:60].round(2)


# QB 2023
df = pd.read_csv('WRS/2023.csv')
df = renameDf(df)
df['Name'] = df['Name'].apply(lambda x: x.split('(')[0].strip() if isinstance(x, str) else x)
df = convertCols(df)
df = newTotal(df)
lastYeardf = getPointsPerGame(df)

# QB 2024
df = pd.read_csv('WRS/2024.csv')
df = renameDf(df)
df = convertCols(df)
df = newTotal(df)
projectedDf = getPointsPerGame(df)

# Final DF
lastYeardf = lastYeardf.rename(columns={'Receiving_Touchdowns': 'Last_Receiving_Touchdowns','Receptions': 'Last_Receptions','Rushing_Touchdowns': 'Last_Rushing_Touchdowns','Rushing_Yards': 'Last_Rushing_Yards','PTS/P/G': 'Last_PTS/P/G',})

lastYeardf["Last_Rankings"] = lastYeardf.index

lastYeardf = lastYeardf[['Name', 'Adjusted_Fantasy_Points', 'Last_Receiving_Touchdowns', 'Last_Receptions', 'Last_Rushing_Touchdowns', 'Last_Rushing_Yards', 'Last_PTS/P/G', 'Last_Rankings']]

merged_df = pd.merge(projectedDf, lastYeardf, on='Name', how='left')

merged_df['Rushing_Yards_Diff'] = merged_df['Rushing_Yards'] - merged_df['Last_Rushing_Yards']
merged_df['Receiving_Touchdowns_Diff'] = merged_df['Receiving_Touchdowns'] - merged_df['Last_Receiving_Touchdowns']
merged_df['Rushing_Touchdowns_Diff'] = merged_df['Rushing_Touchdowns'] - merged_df['Last_Rushing_Touchdowns']
merged_df['Receptions_Diff'] = merged_df['Receptions'] - merged_df['Last_Receptions']

merged_df.index = merged_df.index + 1
merged_df['Rankings'] = merged_df.index
merged_df['Last_Rankings'] = merged_df['Last_Rankings'] + 1

# Merge with different sites
merged_wrs_df = pd.merge(merged_df, sleeperDf, on='Name', how='left')
merged_wrs_df = pd.merge(merged_wrs_df, underDogDf, on='Name', how='left')

merged_wrs_df['Rankings'] = merged_wrs_df.index + 1

merged_wrs_df.rename(columns={
    'Rankings': 'Rk',
    'PosRk_x': 'Sleeper Rk',
    'PosRk_y': 'UnderDog Rk',
}, inplace=True)

# Change types of columns
merged_wrs_df['UnderDog Rk'] = merged_wrs_df['UnderDog Rk'].str.replace('WR', '')
merged_wrs_df['Sleeper Rk'] = merged_wrs_df['Sleeper Rk'].str.replace('WR', '')

merged_wrs_df['Last_Rankings'] = merged_wrs_df['Last_Rankings'].fillna(1000)
merged_wrs_df['UnderDog Rk'] = merged_wrs_df['UnderDog Rk'].fillna(1000)
merged_wrs_df['Sleeper Rk'] = merged_wrs_df['Sleeper Rk'].fillna(1000)

merged_wrs_df = merged_wrs_df.astype({
    'Last_Rankings': 'int',
    'UnderDog Rk': 'int',
    'Sleeper Rk': 'int'
})

merged_wrs_df = merged_wrs_df[[ 'Name', 'Last_Rankings', 'Rk', 'UnderDog Rk', 'Sleeper Rk', 'Last_PTS/P/G', 'PTS/P/G']]