from . feature_engineering_step import FeatureEngineeringStep
from mls_lib.objects.encoders.cat_boost_encoder import CatBoostEncoder
class CatBoostEncoderTrainer(FeatureEngineeringStep):
    def __init__(self, columns, data):
        super().__init__(
            data = data
        )
        self.columns = columns
        self.encoder = CatBoostEncoder()
    
    def fit_transform(self):
        data = self._getInput("data")
        df = data.getData()

        self.encoder.fit_transform(df, self.getColumns())

        data.setData(df)

        self._setOutput("encoder", self.encoder)
        
        self.finishExecution()