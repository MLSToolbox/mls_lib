""" CategoricalBoostEncoderTrainer: Component that trains a categorical boost encoder. """

from mls_lib.objects.encoders.cat_boost_encoder import CategoricalBoostEncoder
from .encoder_trainer import EncoderTrainer

class CatBoostEncoderTrainer(EncoderTrainer):
    """ CategoricalBoostEncoderTrainer: Component that trains a categorical boost encoder. """
    def __init__(self, columns : list) -> None:
        super().__init__(columns)
        self.encoder = CategoricalBoostEncoder()
