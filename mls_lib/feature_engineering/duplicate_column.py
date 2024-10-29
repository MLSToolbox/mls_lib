""" DuplicateColumn: Component that duplicates columns. """

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task

class DuplicateColumn(Task):
    """ DuplicateColumn: Component that duplicates columns. """
    def __init__(self, original_column_name : str, new_column_name : str) -> None:
        super().__init__()
        self.old_table = DataFrame()
        self.original_column_name = original_column_name
        self.new_column_name = new_column_name

    def set_data(self, old_table : DataFrame) -> None:
        """
        Sets the input table to be used for column duplication.
        
        Parameters:
            old_table (DataFrame): The input table from which columns will be duplicated.
        
        Returns:
            None
        """
        self.old_table = old_table

    def execute(self) -> None:
        """
        Executes the function by getting the input dataframe, 
        duplicating the specified column, setting the output dataframe,
        and finishing the execution.

        Parameters:
            None

        Returns:
            None
        """
        data = self.old_table.get_data()
        data[self.new_column_name] = data[self.original_column_name]

        new_df = DataFrame()
        new_df.set_data(data)

        self._set_output("new_table", new_df)
