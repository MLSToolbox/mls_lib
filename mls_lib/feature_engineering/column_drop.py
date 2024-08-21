""" ColumnDrop: Component that drops columns from the input table. """

from . feature_engineering_step import FeatureEngineeringStep

class ColumnDrop(FeatureEngineeringStep):
    """
        ColumnDrop: Drops columns from the input table when executed.
    """
    def __init__(self, origin_table, columns):
        """
        Initializes a ColumnDrop instance with the origin table and columns to be dropped.
        
        Parameters:
            origin_table (object): The origin table from which columns will be dropped.
            columns (list): A list of column names to be dropped from the origin table.
        
        Returns:
            None
        """
        super().__init__(
            origin = origin_table
        )
        self.columns = columns
    def execute(self):
        """
        Executes the function by getting the input dataframe, 
        dropping specified columns, setting the output dataframe,
        and finishing the execution.

        Parameters:
            None

        Returns:
            None
        """
        dataframe = self._get_input("origin")
        data = dataframe.get_data()
        data = data.drop(self.columns, axis=1)
        dataframe.set_data(data)

        self._set_output("resulting_table", dataframe)
        self.finish_execution()
