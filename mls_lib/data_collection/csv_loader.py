""" CSV Loader """

import pandas as pd

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task

class CSVLoader(Task):
    """ CSV Loader """
    def __init__(self, path : str, separator : str) -> None:
        super().__init__()
        self.path = path
        self.separator = separator

    def execute(self) -> None:
        df = DataFrame()
        data = pd.read_csv(self.path, sep = self.separator)
        df.set_data(data)
        self._set_output("out", df)
