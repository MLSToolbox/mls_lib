""" Replace Null Median : Replaces all null values of the
given column with the median of the column """

from mls_lib.orchestration import Task
from mls_lib.objects.data_frame import DataFrame
class ReplaceNullMedian(Task):
    """ Replace Null Median : Replaces all null values of the 
    given column with the median of the column """
    def __init__(self, column : str) -> None:
        super().__init__()
        self.column = column
        self.data_in = DataFrame()

    def set_data(self, data_in : DataFrame) -> None:
        self.data_in = data_in

    def execute(self) -> None:

        df = self.data_in.get_data()

        df[self.column] = df[self.column].fillna(df[self.column].median())

        self.data_in.set_data(df)

        self._set_output("out", self.data_in)
