from ....mls_lib.objects.scalers import MinMaxScaler
from ....mls_lib.objects.data_frame import DataFrame, pd
from pytest import fixture

@fixture
def data_frame():
    return DataFrame()

def test_standard_scaler(data_frame: DataFrame):
    data_frame.set_data(pd.DataFrame([1, 2, 3], columns=['a']))
    scaler = MinMaxScaler()
    scaler.fit_transform(data_frame, ['a'])

    perfect = pd.DataFrame([0, 0.5, 1], columns=['a'])
    assert str(data_frame.get_data()) == str(perfect) 

    data_frame.set_data(pd.DataFrame([4,5,6], columns=['a']))
    scaler.transform(data_frame)
    perfect = pd.DataFrame([1.5, 2, 2.5], columns=['a'])
    assert str(data_frame.get_data()) == str(perfect)