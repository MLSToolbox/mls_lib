""" Replace Null Text : Replaces all null values of the
given column with a given value """

from mls_lib.orchestration import Task
from mls_lib.objects.data_frame import DataFrame
class ReplaceNullText(Task):
    """ Replace Null Text : Replaces all null values of the 
    given column with a given value """
    def __init__(self, column : str, new_value : str) -> None:
        super().__init__()
        self.column = column
        self.new_value = new_value
        self.data_in = DataFrame()

    def set_data(self, data_in : DataFrame) -> None:
        self.data_in = data_in

    def execute(self) -> None:

        df = self.data_in.get_data()

        df[self.column] = df[self.column].fillna(self.new_value)
        
        self.data_in.set_data(df)

        self._set_output("out", self.data_in)
