from ....mls_lib.objects.encoders import LabelEncoder
from ....mls_lib.objects.data_frame import DataFrame, pd

def test_one_hot_encoder():
    l = LabelEncoder()
    assert l

def test_one_hot_encoder_transform():
    l = LabelEncoder()
    df = DataFrame()
    df.set_data(pd.DataFrame({'a': ["hola", "hola", "hola"], 'b': ["hola1", "hola2", "hola3"]}))
    perfect = pd.DataFrame({'a': ["hola", "hola", "hola"], 'b' : [0, 1, 2]})
    new_data = l.fit_transform(df.get_data(), ['b'])
    assert str(new_data) == str(perfect)

    other_data = pd.DataFrame({'a': ["hola", "hola", "hola"], 'b': ["hola3", "hola2", "hola3"]})
    new_data = l.transform(other_data)
    perfect = pd.DataFrame({'a': ["hola", "hola", "hola"], 'b' : [2, 1, 2]})

    assert str(new_data) == str(perfect)
