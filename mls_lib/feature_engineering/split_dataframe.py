""" SplitDataframe:"""

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task

class SplitDataframe(Task):
    """ SplitDataframe:"""
    def __init__(self, columns : list) -> None:
        super().__init__()
        self.table = DataFrame()
        self.columns = columns

    def set_data(self, table : DataFrame) -> None:
        """
        Sets the input table to be used for column selection.

        Parameters:
            input_table (DataFrame): The input table to select columns from.

        Returns:
            None
        """
        self.table = table

    def execute(self) -> None:
        """
        Executes the function by getting the input dataframe,
        splitting it into two datasets given the columns of interest,
        setting the output dataframes,
        and finishing the execution.

        Parameters:
            None

        Returns:
            None
        """
        data = self.table.get_data()
        selected_data = data[self.columns]
        unselected_data = data.drop(self.columns, axis=1)
        
        selected_df = DataFrame()
        selected_df.set_data(selected_data)
        
        unselected_df = DataFrame()
        unselected_df.set_data(unselected_data)

        self._set_output("selected_table", selected_df)
        self._set_output("unselected_table", unselected_df)
