""" Scaler Trainer """

from mls_lib.orchestration.step import Step
from mls_lib.objects.data_frame import DataFrame
from mls_lib.objects.scalers.iscaler import IScaler

class ReuseScaler(Step):
    """ Scaler Trainer """
    def __init__(self) -> None:
        super().__init__()
        self.data = DataFrame()
        self.scaler = IScaler()

    def set_data(self, data : DataFrame, scaler : IScaler) -> None:
        self.data = data
        self.scaler = scaler
    def execute(self):
        self.scaler.transform(self.data)

        new_data = DataFrame()
        new_data.set_data(self.data.get_data())

        self._set_output("out", new_data)
