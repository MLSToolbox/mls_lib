""" Scaler Trainer """

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.step import Step
from mls_lib.objects.scalers.iscaler import IScaler

class ScalerTrainer(Step):
    """ Scaler Trainer """
    def __init__(self, columns : list) -> None:
        super().__init__()
        self.data = DataFrame()
        self.columns = columns
        self.scaler = IScaler()
    
    def set_data(self, data : DataFrame) -> None:
        self.data = data

    def execute(self):
        self.scaler.fit_transform(self.data, self.columns)

        new_data = DataFrame()
        new_data.set_data(self.data.get_data())

        self._set_output("scaler", self.scaler)

        self._set_output("out", new_data)
