from mls_lib.data_cleaning import DataCleaningStep

class ReplaceValue(DataCleaningStep):
    def __init__(self, column, value_map, data_in):
        super().__init__(
            data_in = data_in
        )
        
        self.column = column
        self.value_map = value_map

    def execute(self):
        data = self._getInput("data_in").copy()
        
        df = data.getData()

        df[self.column] = df[self.column].map(self.value_map)
        
        data.setData(df)
        
        self._setOutput("out", data)

        self.finishExecution()

