from mls_lib.data_cleaning import DataCleaningStep

class ReplaceNaN(DataCleaningStep):
    def __init__(self, value, origin):
        super().__init__(
            origin = origin
        )

        self.value = value
        
    def execute(self):
        data = self._getInput("origin")
        
        df = data.getData()
        df = df.fillna(self.value)
        data.setData(df)

        self._setOutput("result", data)

        self.finishExecution()
