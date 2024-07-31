from .data_collection_step import DataCollectionStep
from mls_lib.objects.data_frame import DataFrame
import pandas as pd

class ExcelLoader(DataCollectionStep):
    def __init__(self, path : str):
        super().__init__(),
        self.path = path

    def execute(self):
        df = DataFrame()
        data = pd.read_excel(self.path)
        df.setData(data)
        self._setOutput("resulting_table", df)
        
        self.finishExecution()