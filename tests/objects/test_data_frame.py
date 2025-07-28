from ...mls_lib.objects.data_frame import DataFrame, pd
from pytest import fixture

@fixture
def data_frame():
    return DataFrame()

def test_empty_data_frame(data_frame: DataFrame):
    assert data_frame.get_data() is None

def test_set_data(data_frame: DataFrame):
    data_frame.set_data(pd.DataFrame())
    assert data_frame.get_data() is not None

    data_frame.set_data(None)
    assert data_frame.get_data() is None

    p = pd.DataFrame([1, 2, 3])
    data_frame.set_data(p)
    assert data_frame.get_data().equals(p)

def test_from_np_array(data_frame: DataFrame):
    p = pd.DataFrame([1, 2, 3])
    data_frame.from_np_array([1, 2, 3], None)
    assert data_frame.get_data().equals(p)

def test_get_data(data_frame: DataFrame):
    p = pd.DataFrame([1, 2, 3])
    data_frame.set_data(p)
    assert data_frame.get_data().equals(p)