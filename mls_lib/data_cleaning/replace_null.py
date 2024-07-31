from mls_lib.data_cleaning import DataCleaningStep

class ReplaceNull(DataCleaningStep):
    def __init__(self, value, data_in):
        super().__init__(
            data_in = data_in
        )
        self.value = value

    def execute(self):
        data = self._getInput("data_in")

        df = data.getData()
        df = df.fillna(self.value)
        data.setData(df)

        self._setOutput("out", data)

        self.finishExecution()

