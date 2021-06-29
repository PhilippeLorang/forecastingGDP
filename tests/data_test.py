from numpy.testing import assert_array_equal

from forecastingGDP.data import SERIES_ID, get_data

def test_get_data():
    data = get_data()
    assert len(data) > 0
    assert data.shape[1] == len(SERIES_ID)
