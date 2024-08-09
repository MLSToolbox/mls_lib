""" OneHotEncoder: Component that trains a one hot encoder. """

from category_encoders import OneHotEncoder as OHE

from . encoder import Encoder

class OneHotEncoder(Encoder):
    """ OneHotEncoder: Component that trains a one hot encoder. """
    def __init__(self) -> None:
        super().__init__(OHE())
