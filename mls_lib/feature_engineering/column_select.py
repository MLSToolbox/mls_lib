""" ColumnSelect: Component that selects columns from the input table. """

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.step import Step

class ColumnSelect(Step):
    """ ColumnSelect: Component that selects columns from the input table. """
    def __init__(self, columns : list) -> None:
        super().__init__()
        self.input_table = DataFrame()
        self.columns = columns

    def set_data(self, input_table : DataFrame) -> None:
        """
        Sets the input table to be used for column selection.

        Parameters:
            input_table (DataFrame): The input table to select columns from.

        Returns:
            None
        """
        self.input_table = input_table

    def execute(self) -> None:
        data = self.input_table.get_data()
        data = data[self.columns]

        new_df = DataFrame()
        new_df.set_data(data)

        self._set_output("resulting_table", new_df)
