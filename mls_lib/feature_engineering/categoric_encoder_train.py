from . encoder_trainer import EncoderTrainer
from mls_lib.objects.encoders import CategoricEncoder
class CategoricEncoderTrainer(EncoderTrainer):
    def __init__(self, columns, data):
        super().__init__(columns, data)
        self.encoder = CategoricEncoder()
    
    def fit_transform(self):
        self.encoder.fit_transform(self.data)
        self.__setOutput("encoder", self.encoder)
        