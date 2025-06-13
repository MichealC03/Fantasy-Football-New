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
        'TDS': 'TD'
    }, inplace=True)

    df = df[['Player','YDS', 'TD', 'REC', 'G', 'FPTS', 'FL']]

    df.rename(columns={
        'Player' : 'Name',
        'YDS': 'Receiving_Yards',
        'TD': 'Receiving_Touchdowns',
        'REC': 'Receptions',
        'G': 'Games_Played',
        'FPTS': 'Fantasy_Points',
        'FL': 'Fumbles'
    }, inplace=True)

    return df

def convertCols(df):
    # Convert relevant columns to numeric types
    numeric_columns = [
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
        df['Fumbles'] * Fumbles +
        df['Receptions'] * TEPPR
    )

    return df

def getPointsPerGame(df):
    # Create a new column of pts per game
    df['PTS/P/G'] = df['Adjusted_Fantasy_Points'] / df['Games_Played']

    # sort by pts per game

    df_sorted = df.sort_values(by='PTS/P/G', ascending=False)

    return df_sorted.reset_index(drop=True)[:25].round(2)


# QB 2023
df = pd.read_csv('TES/2023.csv')
df = renameDf(df)
df['Name'] = df['Name'].apply(lambda x: x.split('(')[0].strip() if isinstance(x, str) else x)
df = convertCols(df)
df = newTotal(df)
lastYeardf = getPointsPerGame(df)

# QB 2024
df = pd.read_csv('TES/2024.csv')
df = renameDf(df)
df = convertCols(df)
df = newTotal(df)
projectedDf = getPointsPerGame(df)

# Final DF
lastYeardf = lastYeardf.rename(columns={'Receiving_Touchdowns': 'Last_Receiving_Touchdowns','Receptions': 'Last_Receptions','PTS/P/G': 'Last_PTS/P/G',})

lastYeardf["Last_Rankings"] = lastYeardf.index

lastYeardf = lastYeardf[['Name', 'Adjusted_Fantasy_Points', 'Last_PTS/P/G', 'Last_Rankings']]

merged_df = pd.merge(projectedDf, lastYeardf, on='Name', how='left')

# merged_df['Receiving_Touchdowns_Diff'] = merged_df['Receiving_Touchdowns'] - merged_df['Last_Receiving_Touchdowns']
# merged_df['Receptions_Diff'] = merged_df['Receptions'] - merged_df['Last_Receptions']

merged_df.index = merged_df.index + 1
merged_df['Rankings'] = merged_df.index
merged_df['Last_Rankings'] = merged_df['Last_Rankings'] + 1

# Merge with different sites
merged_tes_df = pd.merge(merged_df, sleeperDf, on='Name', how='left')
merged_tes_df = pd.merge(merged_tes_df, underDogDf, on='Name', how='left')

merged_tes_df['Rankings'] = merged_tes_df.index + 1

merged_tes_df.rename(columns={
    'Rankings': 'Rk',
    'PosRk_x': 'Sleeper Rk',
    'PosRk_y': 'UnderDog Rk',
}, inplace=True)

# Change types of columns
merged_tes_df['UnderDog Rk'] = merged_tes_df['UnderDog Rk'].str.replace('TE', '')
merged_tes_df['Sleeper Rk'] = merged_tes_df['Sleeper Rk'].str.replace('TE', '')

merged_tes_df['Last_Rankings'] = merged_tes_df['Last_Rankings'].fillna(1000)
merged_tes_df['UnderDog Rk'] = merged_tes_df['UnderDog Rk'].fillna(1000)
merged_tes_df['Sleeper Rk'] = merged_tes_df['Sleeper Rk'].fillna(1000)

merged_tes_df = merged_tes_df.astype({
    'Last_Rankings': 'int',
    'UnderDog Rk': 'int',
    'Sleeper Rk': 'int'
})

merged_tes_df = merged_tes_df[[ 'Name', 'Last_Rankings', 'Rk', 'UnderDog Rk', 'Sleeper Rk', 'Last_PTS/P/G', 'PTS/P/G']]