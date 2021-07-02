import pandas as pd
import os

from fredapi import Fred

SERIES = {
    'gdp':'GDPC1',
    'prod_indus':'INDPRO',
    #'Manufacturing Production'
    'BusinessExpectations':'ATLSBUSRGEP',
    'Capacity_Utilization':'TCU',
    #'manuf_ISM':'ISM'

    'Manufacturers_New_Orders':'AMTMNO',
    'New_Orders_Non_defense_capital_good_ex_air':'NEWORDER',
    #'Building_permits'
    #'Housing_Starts'
    #'Construction Spending'
    #'new_car'
    #'Crude Oil Production'
    'Chicago_Fed_Activity_Index':'CFNAI',
    'University_of_Michigan_Consumer_Sentiment':'UMCSENT',
    #Philadelphia FedManufacturing Index

    'Advance_Retail_Sales':'MARTSMPCSM44000USS',
    'Real_Disposable_Personal_Income':'DSPIC96',
    'Personal_Consumption_Expenditure':'PCEC96',

    #Initial Jobless Claims
    'Unemployment_Rate':'UNRATE',
    'Employment_Leve':'CE16OV',
    'Non_farm_payroll':'PAYEMS',
    'Not in Labor Force':'LNU05026648',

    #'Average Hourly Wages'
    'Consumer_Price_Index':'CPIAUCSL',
    'Personal_Consumption_Expenditure_ex_food':'PCEPILFE',
    'Producer_Price_Index':'PPIACO',
    #'Oil Price'
    #'Unit Labour Cost'
    'Imports_Goods_Services':'IEAMGSN',
    'Exports_Goods_Services':'IEAXGS',
    'Imports_Goods_from_China':'IMPCH',


    'BofA_US_High_Yield_Index':'BAMLH0A0HYM2',
    'S&P_500':'SP500',
    'VIX_Volatility':'VIXCLS',
    '10YUST':'DGS10',
    '10YUST_2YUST':'T10Y2Y',
    'US_Dollar Index':'DTWEXAFEGS',
}

SERIES_ID = list(SERIES.values())
FIRST_RELEASE_SUFFIX='_first_release'

AGGREGATION_METHOD = 'avg'
FREQUENCY = 'q'
OBSERVATION_START='1947-01-01'
OUTPUT_TYPE_FIRST_RELEASE = 4
OUTPUT_TYPE_NEW_AND_REVISED = 3
OUTPUT_TYPE_REALTIME = 1
OUTPUT_TYPE_VINTAGE_ALL = 2
REALTIME_START='1940-01-01'

CACHE_LOCATION = os.path.expanduser('~/.forecastingGDP.cache.csv')

FRED = Fred()

def get_data(use_cache=False, include_first_release=False):
    '''Returns a dataframe with GDP related series
    Uses cached CSV at `CACHE_LOCATION` when use_cache is True.
    Includes first release series when include_first_release is True.
    '''
    data = __load_cache() if use_cache else __load_data()
    return data if include_first_release else except_first_release(data)

def __load_data():
    '''Returns data from FRED API'''
    data = {}
    for series_id in SERIES_ID:
        series = __load_series(series_id)
        series_first_release = __load_series_first_release(series_id)
        if series_first_release is None: # SP500 does not have first release information
            series_first_release = series.copy()
        # else:
        #     # filling first release NaN with revised values
        #     temp = series.copy()
        #     temp.loc[series_first_release.index] = series_first_release
        #     series_first_release = temp
        data[series_id] = series
        data[first_release_series_id(series_id)] = series_first_release
    return pd.DataFrame(data)

def __load_series(series_id):
    '''Returns the series of ID `series_id` with a quarter frequency'''
    return FRED.get_series(
        series_id,
        frequency=FREQUENCY,
        observation_start=OBSERVATION_START,
        aggregation_method=AGGREGATION_METHOD,
        output_type=OUTPUT_TYPE_REALTIME,
    )

def __load_series_first_release(series_id):
    '''Returns the series of ID `series_id` with a quarter frequency
    at the time it was first released, or None if such information is
    not available'''

    assert AGGREGATION_METHOD == 'avg'
    try:
        # NOTE: frequency cannot be used when requesting first release
        # (output_type=4), data must be aggregated by quarter manually
        # using `mean`.
        return FRED.get_series(
            series_id,
            observation_start=OBSERVATION_START,
            realtime_start=REALTIME_START,
            output_type=OUTPUT_TYPE_FIRST_RELEASE,
        ).resample('QS-Jan').mean()
    except ValueError:
        return None

def __load_cache():
    '''Returns data cached locally at `CACHE_LOCATION` otherwise cache it from FRED API'''
    try:
        return pd.read_csv(CACHE_LOCATION, index_col=0, parse_dates=[0])
    except FileNotFoundError:
        data = __load_data()
        data.to_csv(CACHE_LOCATION)
        return data

def clear_cache():
    '''Clears data cached locally at `CACHE_LOCATION` if any'''
    try:
        os.remove(CACHE_LOCATION)
    except FileNotFoundError:
        pass

def first_release_series_id(series_id):
    '''Returns the ID of the first released values of a given series'''
    return f'{series_id}{FIRST_RELEASE_SUFFIX}'

def first_release_selector(data):
    return data.columns.str.endswith(FIRST_RELEASE_SUFFIX)

def except_first_release(data):
    '''Returns the data excluding first release series.'''
    return data.loc[:, ~first_release_selector(data)]

def only_first_release(data):
    '''Returns the data excluding revised series.'''
    return data.loc[:, first_release_selector(data)]
