from mls_lib.objects.encoders import Encoder
from category_encoders import CatBoostEncoder
class CategoricEncoder(Encoder):
    def __init__(self) -> None:
        super().__init__(CatBoostEncoder())