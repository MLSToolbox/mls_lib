from .feature_engineering_step import FeatureEngineeringStep
class SelectColumns(FeatureEngineeringStep):
    def __init__(self, columns, origin_table):
        super().__init__(
            origin_table = origin_table
        )
        self.columns = columns

    def execute(self):
        dataframe = self._getInput("origin_table")

        new_df = dataframe.copy()
        data = new_df.getData()
        data = data[self.columns]


        new_df.setData(data)

        self._setOutput("resulting_table", new_df)

        self.finishExecution()