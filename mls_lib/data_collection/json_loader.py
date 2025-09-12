""" JSON Loader """
import pandas as pd
from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task

class JSONLoader(Task):
    """ JSON Loader """
    def __init__(self, path : str):
        super().__init__()
        self.path = path

    def execute(self):
        df = DataFrame()
        data = pd.read_json(self.path)
        df.set_data(data)
        self._set_output("out", df)
