from os.path import isfile
from numpy.testing import assert_array_equal

from forecastingGDP.data import CACHE_LOCATION, SERIES_ID, clear_cache, get_data

def test_get_data():
    data = get_data()
    assert len(data) > 0
    assert data.shape[1] == len(SERIES_ID)

def test_get_data_cached():
    data = get_data()
    data_cached = get_data(use_cache=True)
    assert isfile(CACHE_LOCATION)
    assert data.shape == data_cached.shape
    assert data.index.dtype == data_cached.index.dtype
    assert_array_equal(data.dtypes, data_cached.dtypes)

def test_clear_cache():
    if not isfile(CACHE_LOCATION):
        get_data(use_cache=True)
    assert isfile(CACHE_LOCATION)
    clear_cache()
    assert not isfile(CACHE_LOCATION)
