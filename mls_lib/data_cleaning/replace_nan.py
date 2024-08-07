from mls_lib.data_cleaning import DataCleaningStep
from mls_lib.objects.data_frame import DataFrame
class ReplaceNaN(DataCleaningStep):
    def __init__(self, strategy, column, data_in):
        super().__init__(
            data_in = data_in
        )

        self.strategy = strategy
        self.column = column
        
    def execute(self):
        data = self._getInput("data_in").copy()
        
        df = data.getData()
        df = df.fillna(self.value)
        
        data.setData(df)

        self._setOutput("out", data)

        self.finishExecution()
