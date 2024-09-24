""" OneHotEncoderTrainer: Component that trains a one hot encoder. """

from mls_lib.objects.encoders import OneHotEncoder
from .encoder_trainer import EncoderTrainer

class OneHotEncoderTrainer(EncoderTrainer):
    """ OneHotEncoderTrainer: Component that trains a one hot encoder. """
    def __init__(self, columns):
        super().__init__(columns)

        self.encoder = OneHotEncoder()
    