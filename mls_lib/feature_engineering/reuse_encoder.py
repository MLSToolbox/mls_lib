""" Reuse Encoder """

from mls_lib.orchestration.step import Step

from . feature_engineering_step import FeatureEngineeringStep

class ReuseEncoder(FeatureEngineeringStep):
    """ Reuse Encoder """
    def __init__(self, data : Step, encoder : Step) -> None:
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
