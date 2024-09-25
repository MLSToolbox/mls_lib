""" Replace Null : Replace Null Data Cleaning Step """

from mls_lib.orchestration import Step
from mls_lib.objects.data_frame import DataFrame
class ReplaceNullZero(Step):
    """ Replace Null : Replace Null Data Cleaning Step """
    def __init__(self, column : str) -> None:
        super().__init__(
        )
        self.column = column
        self.data_in = DataFrame()

    def set_data(self, data_in : DataFrame) -> None:
        self.data_in = data_in

    def execute(self) -> None:
        df = self.data_in.get_data()
        
        df[self.column] = df[self.column].fillna(0)
        
        self.data_in.set_data(df)

        self._set_output("out", self.data_in)
