from . encoder import Encoder
from category_encoders import OneHotEncoder as OHE
class OneHotEncoder(Encoder):
    def __init__(self) -> None:
        super().__init__(OHE())