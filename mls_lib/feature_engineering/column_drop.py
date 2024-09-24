""" ColumnDrop: Component that drops columns from the input table. """

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.step import Step

class ColumnDrop(Step):
    """
        ColumnDrop: Drops columns from the input table when executed.
    """
    def __init__(self, columns : list):
        """
        Initializes a ColumnDrop instance with the origin table and columns to be dropped.
        
        Parameters:
            columns (list): A list of column names to be dropped from the origin table.
        
        Returns:
            None
        """
        super().__init__()
        self.origin_table = DataFrame()
        self.columns = columns

    def set_data(self, origin_table : DataFrame) -> None:
        """
        Sets the origin table.

        Parameters:
            origin_table (DataFrame): The origin table from which columns will be dropped.

        Returns:
            None
        """
        self.origin_table = origin_table

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
        data = self.origin_table.get_data()
        data = data.drop(self.columns, axis=1)
        self.origin_table.set_data(data)

        self._set_output("resulting_table", self.origin_table)
