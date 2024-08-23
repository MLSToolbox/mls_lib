""" Encoder Trainer """

from mls_lib.objects.data_frame import DataFrame
from mls_lib.objects.encoders.encoder import IEncoder

from . feature_engineering_step import FeatureEngineeringStep

class EncoderTrainer(FeatureEngineeringStep):
    """ Encoder Trainer """
    def __init__(self, data : DataFrame, encoder : IEncoder) -> None:
        super().__init__(
            data = data,
            encoder = encoder
        )

    def execute(self):
        data = self._get_input("data")
        encoder = self._get_input("encoder")

        df = data.get_data()

        encoder.transform(df)

        data.set_data(df)

        self._set_output("encoder", encoder)

        self._set_output("out", data)
        self._finish_execution()
