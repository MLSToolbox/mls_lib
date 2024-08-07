from . feature_engineering_step import FeatureEngineeringStep
from mls_lib.objects.encoders import OneHotEncoder

class OneHotEncoderTrainer(FeatureEngineeringStep):
    def __init__(self, columns, data):
        super().__init__(
            data = data)
        self.columns = columns
        self.encoder = OneHotEncoder()
    
    def execute(self):
        data = self._getInput("data")
        df = data.getData()

        self.encoder.fit_transform(df, self.columns)

        data.setData(df)

        self._setOutput("encoder", self.encoder)

        self._setOutput("data", data)
        
        self.finishExecution()