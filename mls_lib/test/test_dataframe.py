# tests/test_dataframe.py
import pytest
from mls_lib.objects.data_frame import DataFrame

def test_dataframe_set_and_get_data():
    df = DataFrame()
    data = [[1, 2], [3, 4]]
    df.set_data(data)
    assert df.data == data

