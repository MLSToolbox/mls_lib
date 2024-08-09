""" CSV Loader """

import pandas as pd

from mls_lib.objects.data_frame import DataFrame

from .data_collection_step import DataCollectionStep

class CSVLoader(DataCollectionStep):
    """ CSV Loader """
    def __init__(self, path : str):
        super().__init__()
        self.path = path

    def execute(self):
        df = DataFrame()
        data = pd.read_csv(self.path)
        df.set_data(data)
        self._set_output("out", df)
        self.finish_execution()
