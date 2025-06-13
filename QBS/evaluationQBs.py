import pandas as pd
from sleeper import sleeperDf
from underdog import underDogDf

# init variables
PassingMult = .04
RushingMult = .1
PassingTd = 6
RushingTd = 10
Interceptions = -2
Fumbles = -2


def renameDf(df):
  # Adjustments for predictions
  if 'G' not in df.columns:
      df['G'] = 17
  
  if 'TD' not in df.columns:
      df.rename(columns={
      'TDS': 'TD',
      'INTS': 'INT',
      'TDS.1': 'TD.1',
  }, inplace=True)
  
  df = df[['Player','YDS', 'TD', 'INT', 'YDS.1', 'TD.1', 'G', 'FPTS', 'FL']]
  
  df.rename(columns={
      'Player': 'Name',
      'YDS': 'Passing_Yards',
      'TD': 'Passing_Touchdowns',
      'INT': 'Interceptions',
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
      'Passing_Yards',
      'Passing_Touchdowns',
      'Interceptions',
      'Rushing_Yards',
      'Rushing_Touchdowns',
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
      df['Passing_Yards'] * PassingMult +
      df['Passing_Touchdowns'] * PassingTd +
      df['Rushing_Yards'] * RushingMult +
      df['Rushing_Touchdowns'] * RushingTd +
      df['Interceptions'] * Interceptions + 
      df['Fumbles'] * Fumbles
  )
  
  return df

def getPointsPerGame(df):
  # Create a new column of pts per game
  df['PTS/P/G'] = df['Adjusted_Fantasy_Points'] / df['Games_Played']
  
  # sort by pts per game
  
  df_sorted = df.sort_values(by='PTS/P/G', ascending=False)
  
  return df_sorted.reset_index(drop=True)[:30].round(2)


# QB 2023
df = pd.read_csv('QBS/QB2023Basic.csv')
df = renameDf(df)
df['Name'] = df['Name'].apply(lambda x: x.split('(')[0].strip() if isinstance(x, str) else x)
df = convertCols(df)
df = newTotal(df)
lastYeardf = getPointsPerGame(df)

# QB 2024
df = pd.read_csv('QBS/QB2024Projections.csv')
df = renameDf(df)
df = convertCols(df)
df = newTotal(df)
projectedDf = getPointsPerGame(df)

# Final DF
lastYeardf = lastYeardf.rename(columns={'Passing_Touchdowns': 'Last_Passing_Touchdowns','Interceptions': 'Last_Interceptions','Rushing_Touchdowns': 'Last_Rushing_Touchdowns','PTS/P/G': 'Last_PTS/P/G',})

lastYeardf["Last_Rankings"] = lastYeardf.index

lastYeardf = lastYeardf[['Name', 'Adjusted_Fantasy_Points', 'Last_Passing_Touchdowns', 'Last_Interceptions', 'Last_Rushing_Touchdowns', 'Last_PTS/P/G', 'Last_Rankings']]

merged_df = pd.merge(projectedDf, lastYeardf, on='Name', how='left')

merged_df.index = merged_df.index + 1
merged_df['Rankings'] = merged_df.index
merged_df['Last_Rankings'] = merged_df['Last_Rankings'] + 1

# Merge with different sites
merged_qbs_df = pd.merge(merged_df, sleeperDf, on='Name', how='left')
merged_qbs_df = pd.merge(merged_qbs_df, underDogDf, on='Name', how='left')

merged_qbs_df['Rankings'] = merged_qbs_df.index + 1

merged_qbs_df.rename(columns={
    'Rankings': 'Rk',
    'PosRk_x': 'Sleeper Rk',
    'PosRk_y': 'UnderDog Rk',
}, inplace=True)

# Change types of columns
merged_qbs_df['UnderDog Rk'] = merged_qbs_df['UnderDog Rk'].str.replace('QB', '')
merged_qbs_df['Sleeper Rk'] = merged_qbs_df['Sleeper Rk'].str.replace('QB', '')

merged_qbs_df['Last_Rankings'] = merged_qbs_df['Last_Rankings'].fillna(1000)
merged_qbs_df['UnderDog Rk'] = merged_qbs_df['UnderDog Rk'].fillna(1000)
merged_qbs_df['Sleeper Rk'] = merged_qbs_df['Sleeper Rk'].fillna(1000)

merged_qbs_df = merged_qbs_df.astype({
    'Last_Rankings': 'int',
    'UnderDog Rk': 'int',
    'Sleeper Rk': 'int'
})

merged_qbs_df = merged_qbs_df[[ 'Name', 'Last_Rankings', 'Rk', 'UnderDog Rk', 'Sleeper Rk', 'Last_PTS/P/G', 'PTS/P/G']]