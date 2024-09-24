""" LabelEncoderTrainer: Component that trains a label encoder. """

from mls_lib.objects.encoders import LabelEncoder

from .encoder_trainer import EncoderTrainer

class LabelEncoderTrainer(EncoderTrainer):
    """ LabelEncoderTrainer: Component that trains a label encoder. """
    def __init__(self, columns : list):
        super().__init__(columns)
        self.encoder = LabelEncoder()
    