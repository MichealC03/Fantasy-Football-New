from variables import *
import requests
import pandas as pd

response = requests.get(
      'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3',
      params=params,
      cookies=cookies,
      headers=headers,
  )

  #Turn the response into a json and get the players out of it
  players_dict = response.json()['players']