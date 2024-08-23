""" SelectColumns: Component that selects columns from the input table. """
from .feature_engineering_step import FeatureEngineeringStep
class SelectColumns(FeatureEngineeringStep):
    """ SelectColumns: Component that selects columns from the input table. """
    def __init__(self, columns, origin_table):
        super().__init__(
            origin_table = origin_table
        )
        self.columns = columns

    def execute(self):
        dataframe = self._get_input("origin_table")

        new_df = dataframe.copy()
        data = new_df.get_data()
        data = data[self.columns]


        new_df.set_data(data)

        self._set_output("resulting_table", new_df)

        self._finish_execution()
