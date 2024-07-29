from . encoder_trainer import EncoderTrainer
from mls_lib.mls_lib.objects.encoders import cat_boost_encoder
class CatBoostEncoderTrainer(EncoderTrainer):
    def __init__(self, columns, data):
        super().__init__(columns, data)
        self.encoder = cat_boost_encoder()
    
    def fit_transform(self):
        self.encoder.fit_transform(self.data)
        self.__setOutput("encoder", self.encoder)
        