""" Scaler Trainer """

from mls_lib.objects.data_frame import DataFrame
from mls_lib.objects.scalers.iscaler import IScaler

from . feature_engineering_step import FeatureEngineeringStep

class ReuseScaler(FeatureEngineeringStep):
    """ Scaler Trainer """
    def __init__(self, data : DataFrame, scaler : IScaler) -> None:
        super().__init__(
            data = data,
            scaler = scaler
        )

    def execute(self):
        data = self._get_input("data")
        scaler = self._get_input("scaler")

        scaler.transform(data)

        new_data = DataFrame()
        new_data.set_data(data.get_data())

        self._set_output("out", new_data)
        self._finish_execution()
