from variables import headersFantasyPros, paramsFantasyPros
import requests
import pandas as pd

# Got this from https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php
# the FantasyPros inspect was in Fetch at consensus-rankings?type=draft&scoring=PPR&position=ALL&week=0&experts=available&sport=NFL

# Steps for next year:
# DONT STRESS

# 1. Go to website
# 2. Inspect the page
# 3. Find the API call in the Network tab
# 4. Copy the headers and params from CURL into variables.py
# 5. Shouldnt have to change the code below, just the variables.py file


def fetch_adp_data():
    response = requests.get('https://api.fantasypros.com/v2/json/nfl/2025/consensus-rankings', headers=headersFantasyPros, params=paramsFantasyPros)
    if response.status_code == 200:
        # Parse the JSON response in the players key
        data = response.json()['players']
        #only keep the first 200 players
        data = data[:200]

        print(f"Data fetched successfully: {len(data)} records found.")

        # Convert the data to a DataFrame
        df = pd.DataFrame(data)
        df = df[["player_name", "rank_ecr", "pos_rank", "player_team_id"]]
        df.columns = ["Player", "ADP", "Position", "Team"]

        # clean Player names especially apostrophes
        df = clean_data(df)

        # Sort the DataFrame by ADP
        df.sort_values(by="ADP", inplace=True)
        df.reset_index(drop=True, inplace=True)

        # concatenate the position and rank to create a new column
        df['FP_POSRANK'] = df.groupby('Position').cumcount() + 1
        
        return df
    else:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()
    
def clean_data(fantasyProsDF):
    # drop all rows with NaN in ADP where nan
    fantasyProsDF = fantasyProsDF.dropna(subset=['ADP'])

    # Clean the Player names especially apostrophes
    fantasyProsDF['Player'] = fantasyProsDF['Player'].str.replace("'", "", regex=False)
    fantasyProsDF['Player'] = fantasyProsDF['Player'].str.replace(r'\(.*?\)', '', regex=True).str.strip()

    # Make ecr rank numeric
    fantasyProsDF['ADP_FP'] = pd.to_numeric(fantasyProsDF['ADP'], errors='coerce')

    # Keep only the first two characters of the position
    fantasyProsDF['Position'] = fantasyProsDF['Position'].str[:2]

    # Only keep the positions of QB, RB, WR, TE
    changed_df = fantasyProsDF[fantasyProsDF['Position'].isin(['QB', 'RB', 'WR', 'TE'])]

    return changed_df

fantasyProsDF = fetch_adp_data()
