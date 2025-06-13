import requests
import pandas as pd
import json
from variables import *

def getRowsSharks(cookies, headers, requestURL):
  response = response = requests.get(
      requestURL,
      cookies=cookies,
      headers=headers,
  )

  # Extract the substring containing the relevant data
  start_index = response.text.find('"projections":')  #Start at players key
  end_index = response.text.find('],"teams":',start_index) + 1  #Find the end bracket in the file after the start index
  relevant_data = response.text[start_index: end_index]  #only get the players field

  # Parse the extracted data as JSON and add brackets to the end of the data received from above
  players_data = json.loads('{' + relevant_data + '}')['projections']

  players =[]
  expertRankings = []
  positions = []

  for row in players_data:
    player_row = row['player']
    firstName = player_row['first_name']
    lastName = player_row['last_name']
    positions.append(player_row['position'])
    players.append(firstName + " " + lastName)

    
    expertRankings.append(row['dmvpPPROverallRank'])     #dmvpPPR

  df = pd.DataFrame({'Name' : players})
  df['SharkRanks'] = expertRankings
  df['Positions'] = positions

  # Define the positions to keep
  positions_to_keep = ['RB', 'WR', 'QB', 'TE']

  # Filter the DataFrame to keep only the specified positions
  df = df[df['Positions'].isin(positions_to_keep)]

  df_sorted = df.sort_values(by='SharkRanks', ascending=True)
  df_sorted.reset_index(drop=True, inplace=True)

  df_sorted['SharkRk'] = df_sorted.index + 1

  return df_sorted.head(200)

draftSharksDf = getRowsSharks(cookiesSharks, headersSharks, requestsShark)