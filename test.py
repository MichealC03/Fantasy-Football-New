import requests

headers = {
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9,es-MX;q=0.8,es;q=0.7',
    'priority': 'i',
    'referer': 'https://www.draftsharks.com/',
    'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-storage-access': 'none',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
}

params = {
    'id': '1392162578147274',
    'ev': 'PageView',
    'dl': 'https://www.draftsharks.com/adp/ppr/sleeper/12',
    'rl': 'https://www.bing.com/',
    'if': 'false',
    'ts': '1750616646097',
    'sw': '1920',
    'sh': '1080',
    'v': '2.9.210',
    'r': 'stable',
    'ec': '3',
    'o': '12318',
    'fbp': 'fb.1.1750226438077.76221457573941268',
    'ler': 'other',
    'it': '1750616369561',
    'coo': 'false',
    'exp': 'k0',
    'rqm': 'GET',
}

response = requests.get('https://www.facebook.com/tr/', params=params, headers=headers)

#print(response.text)

#start = response.text.find('{"player_id":')  # Start at players key

print(response.text )