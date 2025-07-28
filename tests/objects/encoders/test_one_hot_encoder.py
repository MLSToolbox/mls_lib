from mls_lib.objects.encoders import OneHotEncoder
from mls_lib.objects.data_frame import DataFrame, pd

def test_one_hot_encoder():
    o = OneHotEncoder([])
    assert o

def test_one_hot_encoder_transform():
    o = OneHotEncoder(['b'])
    df = DataFrame()
    df.set_data(pd.DataFrame({'a': ["hola", "hola", "hola"], 'b': ["hola1", "hola2", "hola3"]}))
    perfect = pd.DataFrame({'a': ["hola", "hola", "hola"], 'b_1':  [1, 0 ,0], 'b_2': [0, 1, 0], 'b_3': [0, 0, 1]})
    new_data = o.fit_transform(df.get_data(), ['b'])

    assert str(new_data) == str(perfect)

    other_data = pd.DataFrame({'a': ["hola", "hola", "hola"], 'b': ["hola3", "hola2", "hola3"]})
    new_data = o.transform(other_data)
    perfect = pd.DataFrame({'a': ["hola", "hola", "hola"], 'b_1':  [0, 0 ,0], 'b_2': [0, 1, 0], 'b_3': [1, 0, 1]})

    assert str(new_data) == str(perfect)
