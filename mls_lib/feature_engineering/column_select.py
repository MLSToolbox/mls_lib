from . feature_engineering_step import FeatureEngineeringStep
class ColumnSelect(FeatureEngineeringStep):
    def __init__(self, input_table, columns):
        super().__init__(
            input_table = input_table
        )
        self.columns = columns

    def execute(self):
        dataframe = self._getInput("input_table")

        data = dataframe.getData()
        data = data[self.columns]

        dataframe.setData(data)

        self._setOutput("resulting_table", dataframe)

        self.finishExecution()