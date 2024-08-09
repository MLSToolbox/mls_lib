""" CategoricalBoostEncoder: Component that trains a categorical boost encoder. """

from category_encoders import CatBoostEncoder as CBE

from . encoder import Encoder

class CategoricalBoostEncoder(Encoder):
    """ CategoricalBoostEncoder: Component that trains a categorical boost encoder. """
    def __init__(self) -> None:
        super().__init__(CBE())
