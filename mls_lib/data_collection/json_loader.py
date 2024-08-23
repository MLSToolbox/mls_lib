""" JSON Loader """
import pandas as pd
from mls_lib.objects.data_frame import DataFrame
from . data_collection_step import DataCollectionStep

class JSONLoader(DataCollectionStep):
    """ JSON Loader """
    def __init__(self, path : str):
        super().__init__()
        self.path = path

    def execute(self):
        df = DataFrame()
        data = pd.read_json(self.path)
        df.set_data(data)
        self._set_output("resulting_table", df)
        self._finish_execution()
