import requests
import pandas as pd
from bs4 import BeautifulSoup

def getBigPlayCatchRow(url, bigPlaysDf):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    player_directory = soup.find(class_='nfl-c-player-directory')
    rows = player_directory.find_all('tr')
    data = []

    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 5:
            player_name = cells[0].text.strip()
            yd_catch_20_plus = pd.to_numeric(cells[4].text.strip(), errors='coerce')
            yd_catch_40_plus = pd.to_numeric(cells[5].text.strip(), errors='coerce')
            if yd_catch_40_plus >= 2 or (yd_catch_40_plus == 1 and yd_catch_20_plus >= 5):
                data.append([player_name, yd_catch_40_plus])

    bigPlaysDf = bigPlaysDf._append(pd.DataFrame(data, columns=['Name', '40+ Yd Catches']))
    bigPlaysDf.reset_index(drop=True, inplace=True)
    return bigPlaysDf

def getBigPlayRushRow(url, rushDf):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    player_directory = soup.find(class_='nfl-c-player-directory')
    rows = player_directory.find_all('tr')
    data = []

    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 5:
            player_name = cells[0].text.strip()
            yd_rush_20_plus = pd.to_numeric(cells[4].text.strip(), errors='coerce')
            yd_rush_40_plus = pd.to_numeric(cells[5].text.strip(), errors='coerce')
            if yd_rush_40_plus >= 2 or (yd_rush_40_plus == 1 and yd_rush_20_plus >= 2):
                data.append([player_name, yd_rush_40_plus])

    rushDf = rushDf._append(pd.DataFrame(data, columns=['Name', '40+ Yd Rush']))
    rushDf.reset_index(drop=True, inplace=True)
    return rushDf

# Initialize DataFrames
bigPlaysDf = pd.DataFrame()
rushDf = pd.DataFrame()

# Populate bigPlaysDf with receiving data
bigPlaysDf = getBigPlayCatchRow("https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receiving40plusyardseach/DESC", bigPlaysDf)
bigPlaysDf = getBigPlayCatchRow("https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receiving40plusyardseach/DESC?aftercursor=AAAAGQAAAA5ACAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXpJaXdpTXpJd01EUm1OR010TkRFMk5TMDVNekkxTFdNeU5Ua3RNREZoTlRJeE1qQXlaVEptSWl3aU1qQXlNeUpkZlE9PQ==", bigPlaysDf)
bigPlaysDf = getBigPlayCatchRow("https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receiving40plusyardseach/DESC?aftercursor=AAAAMgAAACFAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUmlOVFV0TlRBMU15MDBOVGszTFdJNU5UZ3RPRGMwTURoak16RTVOVFptSWl3aU1qQXlNeUpkZlE9PQ==", bigPlaysDf)
bigPlaysDf = getBigPlayCatchRow("https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receiving40plusyardseach/DESC?aftercursor=AAAASwAAAEM_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUXlOVEl0TkdZMU55MDVPVFExTFdGaVpHVXRZMkppTlRjeE9HTTNNalUwSWl3aU1qQXlNeUpkZlE9PQ==", bigPlaysDf)
bigPlaysDf = getBigPlayCatchRow("https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receiving40plusyardseach/DESC?aftercursor=AAAAZAAAAEM_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmhORFV0TkRZME15MDJOekUyTFRaalpqWXRNV1JqWXpReE1EYzFaakZtSWl3aU1qQXlNeUpkZlE9PQ==", bigPlaysDf)
bigPlaysDf = getBigPlayCatchRow("https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receiving40plusyardseach/DESC?aftercursor=AAAAfQAAAEM_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EVXlOR1l0TkRJek5pMDRNall3TFRaa05XWXRZV1UwTjJabE1tVXdNVEk0SWl3aU1qQXlNeUpkZlE9PQ==", bigPlaysDf)

# Populate rushDf with rushing data
rushDf = getBigPlayRushRow("https://www.nfl.com/stats/player-stats/category/rushing/2023/REG/all/rushing40plusyardseach/DESC", rushDf)
rushDf = getBigPlayRushRow("https://www.nfl.com/stats/player-stats/category/rushing/2023/REG/all/rushing40plusyardseach/DESC?aftercursor=AAAAGQAAAA0_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmtORGt0TlRnMU5pMDBNemc0TFdNMk1URXRNRFZpTm1aalptWXhaREZrSWl3aU1qQXlNeUpkZlE9PQ==", rushDf)

bigPlaysDf = pd.merge(bigPlaysDf, rushDf, on='Name', how='outer')

# Fill NaN values with 0 in '40+ Yd Catches' and '40+ Yd Rush'
bigPlaysDf['40+ Yd Catches'].fillna(0, inplace=True)
bigPlaysDf['40+ Yd Rush'].fillna(0, inplace=True)

# Sum the two columns and convert to integer
bigPlaysDf['40+ Yd'] = bigPlaysDf['40+ Yd Catches'] + bigPlaysDf['40+ Yd Rush']

# Drop the original columns if no longer needed
bigPlaysDf.drop(['40+ Yd Catches', '40+ Yd Rush'], axis=1, inplace=True)