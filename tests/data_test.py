from os.path import isfile
from numpy.testing import assert_array_equal

from forecastingGDP.data import CACHE_LOCATION, SERIES_ID, clear_cache, get_data

def test_get_data():
    data = get_data(use_cache=True, include_first_release=True)
    data_cached = get_data(use_cache=True, include_first_release=True)
    assert isfile(CACHE_LOCATION)
    assert len(data) > 0
    assert data.shape[1] == len(SERIES_ID)*2
    assert data.shape == data_cached.shape
    assert data.index.dtype == data_cached.index.dtype
    assert_array_equal(data.dtypes, data_cached.dtypes)

def test_clear_cache():
    if not isfile(CACHE_LOCATION):
        get_data(use_cache=True)
    assert isfile(CACHE_LOCATION)
    clear_cache()
    assert not isfile(CACHE_LOCATION)
