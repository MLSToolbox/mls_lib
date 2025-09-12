""" ReShape: Component that reshapes each entry of the input table. """

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task

class ReShape(Task):
    """ ColumnSelect: Component that reshapes each entry of the input table.  """
    def __init__(self, column: str, dimensions : list) -> None:
        super().__init__()
        self.origin_table = DataFrame()
        self.column = column
        self.dimensions = [int(i) for i in dimensions]

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

        data[self.column] = data[self.column].apply(lambda x: x.reshape(self.dimensions))

        new_df = DataFrame()
        new_df.set_data(data)

        self._set_output("resulting_table", new_df)
