""" LabelEncoderTrainer: Component that trains a label encoder. """

from mls_lib.objects.encoders import LabelEncoder

from . encoder_trainer import EncoderTrainer

class LabelEncoderTrainer(EncoderTrainer):
    """ LabelEncoderTrainer: Component that trains a label encoder. """
    def __init__(self, columns, data):
        super().__init__(
            columns = columns,
            data = data
        )

        self.encoder = LabelEncoder()
    