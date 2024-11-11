""" Model prediction : """
from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task

class ToCSV(Task):
    def __init__(self, path : str) -> None:
        super().__init__()
        self.dataframe = DataFrame()
        self.path = path
    
    def set_data(self, dataframe : DataFrame) -> None:
        self.dataframe = dataframe
    
    def execute(self):
        data = self.dataframe.get_data()
        data.to_csv(self.path)