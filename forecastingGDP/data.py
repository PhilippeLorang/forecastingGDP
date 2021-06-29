import pandas as pd

from fredapi import Fred

SERIES_ID = [
    'GDPC1',

    'AMTMNO',
    'ATLSBUSRGEP',
    'BAMLH0A0HYM2',
    'CCSA',
    'CE16OV',
    'CFNAI',
    'CPIAUCSL',
    'DGS10',
    'DSPIC96',
    'DTWEXAFEGS',
    'ICSA',
    'IEAMGSN',
    'IEAXGS',
    'IMPCH',
    'INDPRO',
    'LNU05026648',
    'MARTSMPCSM44000USS',
    'NEWORDER',
    'PAYEMS',
    'PCEC96',
    'PCEPILFE',
    'PPIACO',
    'SP500',
    'STLFSI2',
    'T10Y2Y',
    'TCU',
    'UMCSENT',
    'UNRATE',
    'VIXCLS',
]

FREQUENCY = 'q'

FRED = Fred()

def get_data():
    '''returns a dataframe with GDP related series'''
    data = {}
    for series_id in SERIES_ID:
        data[series_id] = FRED.get_series(series_id, frequency=FREQUENCY)
    return pd.DataFrame(data)
