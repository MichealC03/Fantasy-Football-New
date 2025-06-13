import requests
from bs4 import BeautifulSoup
import pandas as pd

cookies = {
    'ab_test_global_navigation': 'marauder',
    'fp-cc': 'in',
    '_ga': 'GA1.1.739274071.1721940803',
    '_cc_id': '111910807930949b4b8a794add78baab',
    'OTGPPConsent': 'DBABLA~BVQqAAAACWA.QA',
    '__qca': 'P0-621183946-1721940802439',
    'OptanonAlertBoxClosed': '2024-07-25T20:54:07.333Z',
    'sessionid': '9r5cxoog6kc7yx9gpyf6tz0notzaqit2',
    'is5vHOtZn65zpLqA': '9r5cxoog6kc7yx9gpyf6tz0notzaqit2',
    '33acrossIdTp': 'Dbbf7FtHsu%2F5YKypZLn7YJPpKkKiPkvwOIH1YdpoPWA%3D',
    '_ga_W3D53EQTE0': 'GS1.1.1722295213.8.1.1722295452.47.0.0',
    'ab_test_freestar_ads': 'freestar_ad',
    'fp_recent_visit': '1',
    'fptoken': 'gAAAAABmq8RDdYUfG6LoihQ3D5ALJCKtoaV6WJQN0AmphlXLNzp9HQYdZvf2l0HPC6fi25C-8MQHyMjzywSiLewtK2PJer13gEXyMjlcw6qFq6lbkuIKWpc%3D%3A1722558138',
    'fpdefloc': 'AZ',
    'fp_userdata': 'eyJsYXN0X2xvZ2luIjoiNDUyMjQ5NSIsInVzZXJuYW1lIjoibWljaGVhbGNhbGxhaGFuMjQiLCJlbWFpbCI6Im1pY2hlYWxjYWxsYWhhbjI0QGdtYWlsLmNvbSIsInV1aWQiOiJ1c2VyX2MwMDdhZDJlLTkyYjktNGE0Yi05YzNhLTE3NzIyNzFkZWEzZSIsInBhc3RfcGFpZF9zcG9ydHMiOltdLCJzdWJfbGV2ZWwiOiIiLCJjYW5fZGVwb3NpdF9kcmFmdCI6ZmFsc2UsImNhbl9kZXBvc2l0X2ZhbmR1ZWwiOmZhbHNlLCJkZXBvc2l0X3NpdGVzIjpbIiJdLCJtbGJfbGVhZ3VlcyI6MCwibmZsX2xlYWd1ZXMiOjAsIm5iYV9sZWFndWVzIjowfQ==',
    'fp_level': 'YmFzaWM=',
    'mp_949d2be9e34d246edb7ee4a4cc8720bc_mixpanel': '%7B%22distinct_id%22%3A%20%22user_c007ad2e-92b9-4a4b-9c3a-1772271dea3e%22%2C%22%24device_id%22%3A%20%22190ebab7aa15dd-06b335984c17b6-4c657b58-1fa400-190ebab7aa15dd%22%2C%22%24search_engine%22%3A%20%22bing%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.bing.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.bing.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.bing.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.bing.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24user_id%22%3A%20%22user_c007ad2e-92b9-4a4b-9c3a-1772271dea3e%22%7D',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Aug+02+2024+14%3A09%3A12+GMT-0700+(Mountain+Standard+Time)&version=202311.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&GPPCookiesCount=1&groups=C0003%3A1%2CC0001%3A1%2CC0002%3A1%2CC0004%3A1%2CBG35%3A1&AwaitingReconsent=false&geolocation=US%3BAZ',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'ab_test_global_navigation=marauder; fp-cc=in; _ga=GA1.1.739274071.1721940803; _cc_id=111910807930949b4b8a794add78baab; OTGPPConsent=DBABLA~BVQqAAAACWA.QA; __qca=P0-621183946-1721940802439; OptanonAlertBoxClosed=2024-07-25T20:54:07.333Z; sessionid=9r5cxoog6kc7yx9gpyf6tz0notzaqit2; is5vHOtZn65zpLqA=9r5cxoog6kc7yx9gpyf6tz0notzaqit2; 33acrossIdTp=Dbbf7FtHsu%2F5YKypZLn7YJPpKkKiPkvwOIH1YdpoPWA%3D; _ga_W3D53EQTE0=GS1.1.1722295213.8.1.1722295452.47.0.0; ab_test_freestar_ads=freestar_ad; fp_recent_visit=1; fptoken=gAAAAABmq8RDdYUfG6LoihQ3D5ALJCKtoaV6WJQN0AmphlXLNzp9HQYdZvf2l0HPC6fi25C-8MQHyMjzywSiLewtK2PJer13gEXyMjlcw6qFq6lbkuIKWpc%3D%3A1722558138; fpdefloc=AZ; fp_userdata=eyJsYXN0X2xvZ2luIjoiNDUyMjQ5NSIsInVzZXJuYW1lIjoibWljaGVhbGNhbGxhaGFuMjQiLCJlbWFpbCI6Im1pY2hlYWxjYWxsYWhhbjI0QGdtYWlsLmNvbSIsInV1aWQiOiJ1c2VyX2MwMDdhZDJlLTkyYjktNGE0Yi05YzNhLTE3NzIyNzFkZWEzZSIsInBhc3RfcGFpZF9zcG9ydHMiOltdLCJzdWJfbGV2ZWwiOiIiLCJjYW5fZGVwb3NpdF9kcmFmdCI6ZmFsc2UsImNhbl9kZXBvc2l0X2ZhbmR1ZWwiOmZhbHNlLCJkZXBvc2l0X3NpdGVzIjpbIiJdLCJtbGJfbGVhZ3VlcyI6MCwibmZsX2xlYWd1ZXMiOjAsIm5iYV9sZWFndWVzIjowfQ==; fp_level=YmFzaWM=; mp_949d2be9e34d246edb7ee4a4cc8720bc_mixpanel=%7B%22distinct_id%22%3A%20%22user_c007ad2e-92b9-4a4b-9c3a-1772271dea3e%22%2C%22%24device_id%22%3A%20%22190ebab7aa15dd-06b335984c17b6-4c657b58-1fa400-190ebab7aa15dd%22%2C%22%24search_engine%22%3A%20%22bing%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.bing.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.bing.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.bing.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.bing.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24user_id%22%3A%20%22user_c007ad2e-92b9-4a4b-9c3a-1772271dea3e%22%7D; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Aug+02+2024+14%3A09%3A12+GMT-0700+(Mountain+Standard+Time)&version=202311.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&GPPCookiesCount=1&groups=C0003%3A1%2CC0001%3A1%2CC0002%3A1%2CC0004%3A1%2CBG35%3A1&AwaitingReconsent=false&geolocation=US%3BAZ',
    'origin': 'https://www.fantasypros.com',
    'priority': 'u=0, i',
    'referer': 'https://www.fantasypros.com/nfl/adp/ppr-overall.php',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
}

data = {
    'week': 'draft',
    'expert[]': '4350',
}

response = requests.post('https://www.fantasypros.com/nfl/adp/ppr-overall.php', cookies=cookies, headers=headers, data=data)

soup = BeautifulSoup(response.text, 'html.parser')
player_directory = soup.find(class_='mobile-table mobile-table-report-page')
rows = player_directory.find_all('tr')

# Initialize lists to hold the extracted data
players = []
pos_rks = []
sleeper_adps = []

# Loop through each row and extract the data
for row in rows[1:]:
    cells = row.find_all('td')

    # Extract position rank
    pos_rk_tag = cells[1]
    pos_rk = pos_rk_tag.text if pos_rk_tag else 'N/A'
    if pos_rk.startswith(('K', 'D')):
        continue
    
    # Extract player name
    player_tag = row.find('a', class_='player-name')
    if player_tag:
        player_name = player_tag['fp-player-name']
    else:
        player_name = 'N/A'

    # Append to lists
    players.append(player_name)
    pos_rks.append(pos_rk)

# Create a DataFrame from the extracted data
sleeperDf = pd.DataFrame({
    'Name': players,
    'PosRk': pos_rks
})

sleeperDf['Sleeper ADP'] = sleeperDf.index + 1