""" ColumnSelect: Component that selects columns from the input table. """
from . feature_engineering_step import FeatureEngineeringStep
class ColumnSelect(FeatureEngineeringStep):
    """ ColumnSelect: Component that selects columns from the input table. """
    def __init__(self, input_table, columns):
        super().__init__(
            input_table = input_table
        )
        self.columns = columns

    def execute(self):
        dataframe = self._get_input("input_table")

        data = dataframe.get_data()
        data = data[self.columns]

        dataframe.set_data(data)

        self._set_output("resulting_table", dataframe)

        self.finish_execution()
