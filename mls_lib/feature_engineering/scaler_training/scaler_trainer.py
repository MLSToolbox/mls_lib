""" Scaler Trainer """

import os

import joblib

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task
from mls_lib.objects.scalers.iscaler import IScaler

SCALERS_DIR = "scalers"

class ScalerTrainer(Task):
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

        os.makedirs(SCALERS_DIR, exist_ok=True)
        scaler_name = "_".join(self.columns)
        scaler_path = os.path.join(SCALERS_DIR, f"{scaler_name}.pkl")
        joblib.dump(self.scaler, scaler_path)
    

        self._set_output("scaler", self.scaler)

        self._set_output("out", new_data)
