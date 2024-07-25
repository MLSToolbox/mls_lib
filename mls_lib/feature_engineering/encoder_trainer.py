from . feature_engineering_step import FeatureEngineeringStep

class EncoderTrainer(FeatureEngineeringStep):
    def __init__(self, columns, data):
        super().__init__()
        self.columns = columns
        self.data = data
        self.encoder = None

    def execute(self):
        data_origin, port = self.data
        dataframe = data_origin.get(port)
        data = dataframe.getData()

        encoder_origin, port = self.encoder
        encoder = encoder_origin.get(port)

        encoder.fit_transform(data, self.columns)

        dataframe.setData(data)
        self.outputs["encoder"] = encoder

        self.outputs["data"] = dataframe
    
    def fit_transform(self):
        pass