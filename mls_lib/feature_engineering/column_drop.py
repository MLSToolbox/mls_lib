from . feature_engineering_step import FeatureEngineeringStep

class ColumnDrop(FeatureEngineeringStep):
    def __init__(self, origin_table, columns):
        super().__init__(
            origin = origin_table
        )
        
        self.columns = columns
        
    def execute(self):
        dataframe = self._getInput("origin")
        
        data = dataframe.getData()
        data = data.drop(self.columns, axis=1)
        dataframe.setData(data)

        self._setOutput("resulting_table", dataframe)

        self.finishExecution()