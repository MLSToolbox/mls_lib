from . feature_engineering_step import FeatureEngineeringStep
from mls_lib.objects.encoders import OneHotEncoder

class OneHotEncoderTrainer(FeatureEngineeringStep):
    def __init__(self, columns, data):
        super().__init__(columns, data)
        self.encoder = OneHotEncoder()
    
    def fit_transform(self):
        self.encoder.fit_transform(self.data)
        self.__setOutput("encoder", self.encoder)
        