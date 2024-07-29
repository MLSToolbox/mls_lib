from . encoder import Encoder
from category_encoders import CatBoostEncoder
class CategoricalBoostEncoder(Encoder):
    def __init__(self) -> None:
        super().__init__(CatBoostEncoder())