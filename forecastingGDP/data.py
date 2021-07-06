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
    'New_Orders_Durable_Good':'DGORDER', #updated
    #'New_Orders_Non_defense_capital_good_ex_air':'NEWORDER',
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
    'Personal_Consumption_Expenditure':'PCE',# old PCEC96

    #Initial Jobless Claims
    'Unemployment_Rate':'U1RATE',#old  UNRATE
    'Employment_Leve':'CE16OV',
    'Non_farm_payroll':'PAYEMS',
    'Not in Labor Force':'LNU05026648',

    #'Average Hourly Wages'
    'Consumer_Price_Index':'CPIAUCSL',
    'Personal_Consumption_Expenditure_ex_food':'PCEPILFE',
    'Producer_Price_Index':'PPIACO',
    #'Oil Price'
    #'Unit Labour Cost'
    # 'Imports_Goods_Services':'IEAMGSN',
    # 'Exports_Goods_Services':'IEAXGS',
    'Imports_Goods_Services':'IMPGSC1',#updated
    'Exports_Goods_Services':'EXPGSC1',#updated

    'Imports_Goods_from_China':'IMPCH',


    'BofA_US_High_Yield_Index':'BAMLH0A0HYM2',
    'S&P_500':'SP500',
    'Wilshire_5000_Market_Cap':'WILL5000INDFC',#updated
    'VIX_Volatility':'VIXCLS',
    '10YUST':'GS10', # old DGS10
    '10YUST_2YUST':'GS2',#old T10Y2Y
    'US_Dollar Index':'DTWEXAFEGS',
}

SERIES_ID = list(SERIES.values())
FIRST_RELEASE_SUFFIX='_first_release'

FREQUENCY = 'm' # Monthly, beginning of the month
FREQUENCIES = ['w', 'm', 'q'] # supported frequencies

OBSERVATION_START = '1971-01-01'
OBSERVATION_END = '2021-04-01'

OUTPUT_TYPE_REALTIME = 1
OUTPUT_TYPE_VINTAGE_ALL = 2
OUTPUT_TYPE_NEW_AND_REVISED = 3
OUTPUT_TYPE_FIRST_RELEASE = 4
REALTIME_START = '1940-01-01'

UPSCALING_METHOD='ffill'

CACHE_INFO_LOCATION = os.path.expanduser('~/.forecastingGDP_info.cache.csv')

FRED = Fred()

def get_data(frequency=FREQUENCY, use_cache=False, include_first_release=False):
    '''Returns a dataframe with GDP related series
    Uses cached CSV at `CACHE_LOCATION` when use_cache is True.
    Includes first release series when include_first_release is True.
    '''
    assert frequency in FREQUENCIES
    data = __load_cache(frequency) if use_cache else __load_data(frequency)
    return data if include_first_release else except_first_release(data)

def get_data_info(use_cache=False):
    return __load_cache_info() if use_cache else __load_data_info()

def __load_data(frequency):
    '''Returns data from FRED API'''
    data = {}
    for series_id in SERIES_ID:
        series = get_series(series_id, frequency)
        series_first_release = get_series_first_release(series_id, frequency)
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

def __load_data_info():
    '''Returns data series description from FRED API'''
    return pd.concat([get_series_info(series_id) for series_id in SERIES_ID], axis=1).T.set_index('id')

def get_series(series_id, frequency=FREQUENCY):
    '''Returns the series of ID `series_id` with its 'natural' frequency'''
    return resample_series(
        FRED.get_series(
            series_id,
            observation_start=OBSERVATION_START,
            observation_end=OBSERVATION_END,
            output_type=OUTPUT_TYPE_REALTIME,
        ),
        frequency,
    )

def get_series_first_release(series_id, frequency=FREQUENCY):
    '''Returns the series of ID `series_id` with its 'natural' frequency
    at the time it was first released, or None if such information is
    not available'''
    try:
        return resample_series(
            FRED.get_series(
                series_id,
                observation_start=OBSERVATION_START,
                observation_end=OBSERVATION_END,
                realtime_start=REALTIME_START,
                output_type=OUTPUT_TYPE_FIRST_RELEASE,
            ),
            frequency,
        )
    except ValueError:
        return None

def get_series_info(series_id):
    '''Returns a one row dataframe that describes the series `series_id`.'''
    return FRED.get_series_info(series_id)

def __load_cache(frequency):
    '''Returns data cached locally at `CACHE_LOCATION` otherwise cache it from FRED API'''
    cache = cache_location(frequency)
    try:
        return pd.read_csv(cache, index_col=0, parse_dates=[0])
    except FileNotFoundError:
        data = __load_data(frequency)
        data.to_csv(cache)
        return data

def __load_cache_info():
    '''Returns data description cached locally at `CACHE_INFO_LOCATION` otherwise cache it from FRED API'''
    try:
        return pd.read_csv(CACHE_INFO_LOCATION, index_col=0)
    except FileNotFoundError:
        info = __load_data_info()
        info.to_csv(CACHE_INFO_LOCATION)
        return info

def cache_location(frequency=FREQUENCY):
    return os.path.expanduser(f'~/.forecastingGDP.{frequency}.cache.csv')

def cache_locations():
    return [cache_location(frequency) for frequency in FREQUENCIES]

def clear_cache():
    '''Clears data cached locally if any'''
    for cache in cache_locations() + [CACHE_INFO_LOCATION]:
        try:
            os.remove(cache)
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

def resample_series(series, frequency):
    '''Returns a series or dataframe resampled to the wanted frequency'''
    freq_src = guess_series_frequency(series)
    freq_cmp = compare_freq(frequency, freq_src)
    if freq_cmp > 0:
        return downsample_series(series, frequency)
    if freq_cmp < 0:
        return upsample_series(series, frequency)
    return series

def downsample_series(series, frequency):
    return series.resample(freq_to_pd_fred(frequency)).mean()

def upsample_series(series, frequency):
    # Forward filling avoids data leakage: time or linear
    # interpolation would result in a data leak.
    return series.resample(freq_to_pd_fred(frequency)).interpolate(method=UPSCALING_METHOD)

__FREQUENCY_CONVERSION = {
    'w': 'W-Fri',
    'm': 'MS',
    'q': 'QS-Jan',
}

__FREQUENCY_ORDER = ['d', 'w', 'm', 'q']

def guess_series_frequency(series):
    return pd_freq_to_freq(pd.infer_freq(series.index) or 'd') # BAMLH0A0HYM2

def freq_to_pd_fred(frequency):
    return __FREQUENCY_CONVERSION[frequency]

def pd_freq_to_freq(frequency):
    frequency = frequency.lower()
    if frequency.startswith('q'):
        return 'q'
    if frequency.startswith('m'):
        return 'm'
    if frequency.startswith('d') or frequency.startswith('b'):
        return 'd'
    if frequency.startswith('w'):
        return 'w'
    return None

def compare_freq(frequency_1, frequency_2):
    return __FREQUENCY_ORDER.index(frequency_1) - __FREQUENCY_ORDER.index(frequency_2)
