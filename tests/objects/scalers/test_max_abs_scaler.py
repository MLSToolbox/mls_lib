from ....mls_lib.objects.scalers import MaxAbsScaler
from ....mls_lib.objects.data_frame import DataFrame, pd
from pytest import fixture

@fixture
def data_frame():
    return DataFrame()

def test_standard_scaler(data_frame: DataFrame):
    data_frame.set_data(pd.DataFrame([1, 2, 3], columns=['a']))
    scaler = MaxAbsScaler()
    scaler.fit_transform(data_frame, ['a'])

    perfect = pd.DataFrame([0.333333, 0.666667, 1], columns=['a'])
    assert str(data_frame.get_data()) == str(perfect) 

    data_frame.set_data(pd.DataFrame([4,5,6], columns=['a']))
    scaler.transform(data_frame)
    perfect = pd.DataFrame([1.333333, 1.666667, 2], columns=['a'])
    assert str(data_frame.get_data()) == str(perfect)