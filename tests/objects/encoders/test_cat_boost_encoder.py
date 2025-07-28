from ....mls_lib.objects.encoders import CategoricalBoostEncoder
from ....mls_lib.objects.data_frame import DataFrame, pd

def test_cat_boost_encoder():
    c = CategoricalBoostEncoder()
    assert c

def test_cat_boost_encoder_transform():
    c = CategoricalBoostEncoder()
    df = DataFrame()
    df.set_data(pd.DataFrame({'a': ["hola", "hola", "hola"], 'b': ["hola1", "hola2", "hola3"]}))
    perfect = pd.DataFrame({'a': [1, 0.5, 0.666667], 'b': [1.0,1.0, 1.0]})
    new_data = c.fit_transform(df.get_data(), ['0', 'a', 'b'])
    assert str(new_data) == str(perfect)

    other_data = pd.DataFrame({'a': ["hola", "hola", "hola"], 'b': ["hola3", "hola2", "hola1"]})
    new_data = c.transform(other_data)
    assert str(new_data) == str(perfect)
