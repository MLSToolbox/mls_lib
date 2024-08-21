""" Encoder Trainer """

from . feature_engineering_step import FeatureEngineeringStep

class EncoderTrainer(FeatureEngineeringStep):
    """ Encoder Trainer """
    def __init__(self, columns, data, encoder) -> None:
        super().__init__(data = data)
        self.columns = columns
        self.encoder = encoder

    def execute(self):
        data = self._get_input("data")
        df = data.get_data()

        self.encoder.fit_transform(df, self.columns)

        data.set_data(df)

        self._set_output("encoder", self.encoder)

        self._set_output("out", data)
        self.finish_execution()
