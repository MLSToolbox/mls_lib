""" ColumnSelect: Component that selects columns from the input table. """

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task

class ColumnSelect(Task):
    """ ColumnSelect: Component that selects columns from the input table. """
    def __init__(self, columns : list) -> None:
        super().__init__()
        self.origin_table = DataFrame()
        self.columns = columns

    def set_data(self, origin_table : DataFrame) -> None:
        """
        Sets the input table to be used for column selection.

        Parameters:
            input_table (DataFrame): The input table to select columns from.

        Returns:
            None
        """
        self.origin_table = origin_table

    def execute(self) -> None:
        data = self.origin_table.get_data()
        data = data[self.columns]

        new_df = DataFrame()
        new_df.set_data(data)

        self._set_output("resulting_table", new_df)
