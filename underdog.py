import requests
from variables import *
import pandas as pd


response = requests.post(
  requestsUnderdog,
  headers=headersUnderdog,
  json=jsonDataUnderdog,
)

data = response.json()['response']['table']['data']

underDogDf = pd.DataFrame(data)

underDogDf.loc[underDogDf['Name'] == 'Deebo Samuel', 'Name'] = 'Deebo Samuel Sr.'

underDogDf['UnderDog ADP'] = underDogDf.index + 1
#underDogDf['UnderDog ADP'] = pd.to_numeric(underDogDf['UnderDog ADP'], errors='coerce').astype('Int64')

underDogDf = underDogDf[['Name', 'PosRk', 'UnderDog ADP']]