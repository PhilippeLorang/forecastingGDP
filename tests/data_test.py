from os.path import isfile
from numpy.testing import assert_array_equal

from forecastingGDP.data import CACHE_LOCATION, CACHE_INFO_LOCATION, SERIES_ID, clear_cache, get_data, get_data_info

def test_get_data():
    data = get_data(use_cache=True, include_first_release=True)
    data_cached = get_data(use_cache=True, include_first_release=True)
    assert isfile(CACHE_LOCATION)
    assert len(data) > 0
    assert data.shape[1] == len(SERIES_ID)*2
    assert data.shape == data_cached.shape
    assert data.index.dtype == data_cached.index.dtype
    assert_array_equal(data.dtypes, data_cached.dtypes)

# def test_get_data_info():
#     info = get_data_info()
#     assert len(info) == len(SERIES_ID)
#     assert info.index.name == 'id'
#     assert_array_equal(
#         info.index.to_list(),
#         SERIES_ID,
#     )
#     assert_array_equal(
#         info.columns,
#         [
#             'realtime_start',
#             'realtime_end',
#             'title',
#             'observation_start',
#             'observation_end',
#             'frequency',
#             'frequency_short',
#             'units',
#             'units_short',
#             'seasonal_adjustment',
#             'seasonal_adjustment_short',
#             'last_updated',
#             'popularity',
#             'notes',
#         ],
#     )

def test_clear_cache():
    if not isfile(CACHE_LOCATION):
        get_data(use_cache=True)
    assert isfile(CACHE_LOCATION)
    clear_cache()
    assert not isfile(CACHE_LOCATION)
    assert not isfile(CACHE_INFO_LOCATION)
