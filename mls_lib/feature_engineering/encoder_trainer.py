""" Encoder Trainer """

from mls_lib.orchestration.step import Step
from mls_lib.objects.encoders.encoder import IEncoder

from . feature_engineering_step import FeatureEngineeringStep

class EncoderTrainer(FeatureEngineeringStep):
    """ Encoder Trainer """
    def __init__(self, columns : list, data : Step) -> None:
        super().__init__(data = data)
        self.columns = columns
        self.encoder = IEncoder()

    def execute(self):
        data = self._get_input("data")
        df = data.get_data()

        self.encoder.fit_transform(df, self.columns)

        data.set_data(df)

        self._set_output("encoder", self.encoder)

        self._set_output("out", data)
        self._finish_execution()
