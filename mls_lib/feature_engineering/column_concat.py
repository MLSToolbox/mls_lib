""" ColumnConcat: Component that concatenates two tables. """

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task
import pandas as pd

class ColumnConcat(Task):
    """ ColumnConcat: Component that concatenates two tables. """
    def __init__(self) -> None:
        super().__init__()
        self.left_table = DataFrame()
        self.right_table = DataFrame()
    def set_data(self, left_table : DataFrame, right_table : DataFrame) -> None:
        """
        Sets the input tables to be used for column concatenation.

        Parameters:
            left_table (DataFrame): The left table to be used for column concatenation.
            right_table (DataFrame): The right table to be used for column concatenation.

        Returns:
            None
        """
        self.left_table = left_table
        self.right_table = right_table
    def execute(self) -> None:
        """
        Executes the function by getting the input dataframes,
        concatenating them by column, setting the output dataframe,
        and finishing the execution.

        Parameters:
            None

        Returns:
            None
        """
        left_data = self.left_table.get_data()
        right_data = self.right_table.get_data()
        
        data = pd.concat([left_data, right_data], axis=1)
        
        joined_df = DataFrame()
        joined_df.set_data(data)

        self._set_output("selected_table", joined_df)
