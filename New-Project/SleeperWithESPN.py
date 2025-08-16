import requests
import pandas as pd
from bs4 import BeautifulSoup
from variables import headersSleeperESPN, cookiesSleeperESPN

# Got this from https://www.fantasypros.com/nfl/adp/ppr-overall.php
# Steps for next year:
# 1. Go to website
# 2. Inspect the page
# 3. Find the API call in the Network tab under Doc


def fetch_adp_data():
    url = 'https://www.fantasypros.com/nfl/adp/ppr-overall.php'
    response = requests.get(url, cookies=cookiesSleeperESPN, headers=headersSleeperESPN)

    if response.status_code == 200:
        # Get the html table from the response
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.select_one("div.mobile-table-report-page table")
        rows = table.select("tbody tr")

        data = []
        for row in rows:
            # Skip rows that do not have enough columns
            cols = row.find_all("td")
            if not cols or len(cols) < 7:
                continue

            player_td = cols[1]
            pos = cols[2].text.strip()

            # Skip kickers and defenses
            if pos.startswith("K") or pos.startswith("DST") or pos.startswith("DS"):
                continue
            else:
                pos = pos[:2]

            name = player_td.a.text.strip()
            # Clean the player name
            name = name.replace("'", "").strip()

            # Convert string "nan" to actual None
            espn = cols[3].text.strip()
            sleeper = cols[4].text.strip()
            
            espn = None if espn == "nan" or espn == "" else espn
            sleeper = None if sleeper == "nan" or sleeper == "" else sleeper

            data.append([name, pos, espn, sleeper])

            # end after 200 players
            if len(data) >= 200:
                break

        df = pd.DataFrame(data, columns=["Player", "POS", "ADP_ESPN", "ADP_Sleeper"])

        

        df = get_adps(df)

        return df

def create_espn_POSRANK(df):
    # Purpose: Create a new column for ESPN position rank

    df.sort_values(by='ADP_ESPN', inplace=True)

    df['ESPN_POSRANK'] = df.groupby('POS').cumcount() + 1
    df['ESPN_POSRANK'] = df['ESPN_POSRANK'].astype('Int64', errors='ignore')
    #df['ESPN_POSRANK'] = df['POS'].str[:2] + df['ESPN_POSRANK'].astype(str)

    # Sort by ESPN position rank
    df.sort_values(by='ESPN_POSRANK', inplace=True)

    return df

def create_sleeper_POSRANK(df):
    # Purpose: Create a new column for Sleeper position rank

    df.sort_values(by='ADP_Sleeper', inplace=True)
    df['Sleeper_POSRANK'] = df.groupby('POS').cumcount() + 1

    df['Sleeper_POSRANK'] = df['Sleeper_POSRANK'].astype('Int64', errors='ignore')
    #df['Sleeper_POSRANK'] = df['POS'].str[:2] + df['Sleeper_POSRANK'].astype(str)

    # Sort by Sleeper position rank
    df.sort_values(by='Sleeper_POSRANK', inplace=True)
    return df

def get_adps(df):
    # Purpose: Get the ADP data from FantasyPros and create ESPN and Sleeper position ranks
    
    # make ints not floats
    df['ADP_ESPN'] = df['ADP_ESPN'].astype('Int64', errors='ignore')
    df['ADP_Sleeper'] = df['ADP_Sleeper'].astype('Int64', errors='ignore')
    
    # Then drop rows with actual NaN values
    df = df.dropna(subset=['ADP_ESPN', 'ADP_Sleeper'])
    df = df.reset_index(drop=True)

    df = create_espn_POSRANK(df)
    df = create_sleeper_POSRANK(df)

    df.sort_values(by='ADP_ESPN', inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


# MAIN EXECUTION
sleeperESPNDF = pd.DataFrame()
sleeperESPNDF = fetch_adp_data()

# filter df to only RB
#sleeperESPNDF = sleeperESPNDF[sleeperESPNDF['POS'].isin(['WR'])]

# print to a txt file
#sleeperESPNDF['Player'].to_csv('sleeperESPNDF_WR.csv', index=False)