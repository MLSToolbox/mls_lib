""" Map: Component that changes the value of each element in a column given a dictionary. """

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task

class Map(Task):
    """ Map: Component that changes the value of each element in a column given a dictionary. """
    def __init__(self, target_col: str, index_col: str) -> None:
        super().__init__()
        self.origin_table = DataFrame()
        self.index = DataFrame()
        self.target_column = target_col
        self.index_column = index_col

    def set_data(self, origin_table : DataFrame, index : DataFrame) -> None:
        """
        Sets the input table to be used for column selection.

        Parameters:
            input_table (DataFrame): The input table to select columns from.
            index (DataFrame): The input table to select columns from.

        Returns:
            None
        """
        self.origin_table = origin_table
        self.index = index

    def execute(self) -> None:
        data = self.origin_table.get_data()
        index_data = self.index.get_data()
        max_x = len(index_data[self.index_column])
        data[self.target_column] = data[self.target_column].apply(
            lambda x: index_data[self.index_column].values[min(max_x - 1, round(x))])

        new_df = DataFrame()
        new_df.set_data(data)

        self._set_output("resulting_table", new_df)
