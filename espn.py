import requests
import pandas as pd
from variables import *
from bigPlays import bigPlaysDf
from underdog import underDogDf
from sleeper import sleeperDf
import TES.evaluationTEs
import QBS.evaluationQBs
import RBS.evaluationRBs
import WRS.evaluationWRs
from draftSharks import draftSharksDf

#Get the rows for ESPN (they are split into 50)
def getRowsESPN(cookies, headers, params, start):

  response = requests.get(
      'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/3',
      params=params,
      cookies=cookies,
      headers=headers,
  )

  #Turn the response into a json and get the players out of it
  players_dict = response.json()['players']

  playerList = []
  statsList = []

  #For each player add the player key into the empty list
  for row in players_dict:
    #Get everything about the player info
    inner_player = row['player']

    #Get the team name only for D/ST which is the second to last before end
    if (inner_player['defaultPositionId'] == 16):
      defense = str(inner_player['fullName']).split()
      inner_player['fullName'] = defense[-2]

    playerList.append(inner_player)

    # Get the projected Total for the year and round to 2 decimals
    inner_stat = inner_player['stats']
    stats = str(inner_stat).split()
    projectedTotal = float((stats[3])[:-1])
    statsList.append("{:.2f}".format(projectedTotal))

  # Change the list of players to a dataframe
  df = pd.DataFrame(playerList)

  #Choose and import to display final project
  df = df[['fullName', "defaultPositionId"]]
  df.rename(columns={"fullName": "Name"}, inplace=True)
  df["Projected Totals"] = statsList

  #Drop kickers
  kickers = df[df['defaultPositionId'] == 5].index
  df.drop(kickers, inplace=True)

  defense = df[df['defaultPositionId'] == 16].index
  df.drop(defense, inplace=True)
  
  df.reset_index(drop=True, inplace=True)

  df.index += start

  #Set espn picks = to the index
  df["ESPN Pick"] = df.index

  def get_position(id_value):
    if id_value == 1:
        return 'QB'
    elif id_value == 2:
        return 'RB'
    elif id_value == 3:
        return 'WR'
    elif id_value == 4:
        return 'TE'
    else:
        return 'Unknown'

  # Apply the function to create the Position column
  df['Position'] = df['defaultPositionId'].apply(get_position)

  df = df.drop(columns=['defaultPositionId'])

  return df[['Name', 'Position', 'ESPN Pick', 'Projected Totals']]

df = pd.DataFrame()

df = df._append(getRowsESPN(cookies50, headers50, params50, 1))
df = df._append(getRowsESPN(cookies100, headers100, params100, df.index[-1] + 1))
df = df._append(getRowsESPN(cookies150, headers150, params150, df.index[-1] + 1))
df = df._append(getRowsESPN(cookies200, headers200, params200, df.index[-1] + 1))
df = df._append(getRowsESPN(cookies250, headers250, params250, df.index[-1] + 1))
df = df._append(getRowsESPN(cookies300, headers300, params300, df.index[-1] + 1))

df = pd.merge(df, bigPlaysDf, on='Name', how='left')

#df['40+ Yd'] = pd.to_numeric(df['40+ Yd'], errors='coerce').astype('Int64')

# get the adjusted fantasy points for each player
dfAdjustedAppoints = pd.DataFrame()
dfAdjustedAppoints = dfAdjustedAppoints._append(QBS.evaluationQBs.projectedDf[['Name', 'Adjusted_Fantasy_Points']])
dfAdjustedAppoints = dfAdjustedAppoints._append(RBS.evaluationRBs.projectedDf[['Name', 'Adjusted_Fantasy_Points']])
dfAdjustedAppoints = dfAdjustedAppoints._append(WRS.evaluationWRs.projectedDf[['Name', 'Adjusted_Fantasy_Points']])
dfAdjustedAppoints = dfAdjustedAppoints._append(TES.evaluationTEs.projectedDf[['Name', 'Adjusted_Fantasy_Points']])

df = pd.merge(df, underDogDf[['Name', 'UnderDog ADP']], on='Name', how='left')
df = pd.merge(df, sleeperDf[['Name', 'Sleeper ADP']], on='Name', how='left')
df = pd.merge(df, dfAdjustedAppoints[['Name', 'Adjusted_Fantasy_Points']], on='Name', how='left')
df = pd.merge(df, draftSharksDf[['Name', 'SharkRk']], on='Name', how='left')

df['UnderDog ADP'] = df['UnderDog ADP'].fillna(1000)
df['Sleeper ADP'] = df['Sleeper ADP'].fillna(1000)
df['SharkRk'] = df['SharkRk'].fillna(1000)
df['40+ Yd'] = df['40+ Yd'].fillna(0)
df['Adjusted_Fantasy_Points'] = df['Adjusted_Fantasy_Points'].fillna(0)

df = df.astype({
    '40+ Yd': 'int',
    'SharkRk': 'int',
    'UnderDog ADP': 'int',
    'Sleeper ADP': 'int',
})

df = df[['Name', 'Position', 'Sleeper ADP', 'ESPN Pick', 'SharkRk', 'Adjusted_Fantasy_Points', '40+ Yd' ]]