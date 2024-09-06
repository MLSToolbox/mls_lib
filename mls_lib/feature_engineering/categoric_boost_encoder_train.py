""" CategoricalBoostEncoderTrainer: Component that trains a categorical boost encoder. """

from mls_lib.objects.encoders.cat_boost_encoder import CategoricalBoostEncoder

from . encoder_trainer import EncoderTrainer

class CatBoostEncoderTrainer(EncoderTrainer):
    """ CategoricalBoostEncoderTrainer: Component that trains a categorical boost encoder. """
    def __init__(self, columns, data):
        super().__init__(
            columns = columns,
            data = data
        )

        self.encoder = CategoricalBoostEncoder()
