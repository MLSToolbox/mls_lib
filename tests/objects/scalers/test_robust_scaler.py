from ....mls_lib.objects.scalers import RobustScaler
from ....mls_lib.objects.data_frame import DataFrame, pd
from pytest import fixture

@fixture
def data_frame():
    return DataFrame()

def test_standard_scaler(data_frame: DataFrame):
    data_frame.set_data(pd.DataFrame([1, 2, 3], columns=['a']))
    scaler = RobustScaler()
    scaler.fit_transform(data_frame, ['a'])

    perfect = pd.DataFrame([-1.0, 0.0, 1.0], columns=['a'])
    
    assert str(data_frame.get_data()) == str(perfect) 

    data_frame.set_data(pd.DataFrame([4,5,6], columns=['a']))
    scaler.transform(data_frame)
    perfect = pd.DataFrame([2.0, 3.0, 4.0], columns=['a'])
    assert str(data_frame.get_data()) == str(perfect)