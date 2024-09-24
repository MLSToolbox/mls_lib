""" Replace Null : Replace Null Data Cleaning Step """

from mls_lib.orchestration import Step
from mls_lib.objects.data_frame import DataFrame
class ReplaceNull(Step):
    """ Replace Null : Replace Null Data Cleaning Step """
    def __init__(self, strategy : str, column : str) -> None:
        super().__init__(
        )
        self.strategy = strategy
        self.column = column
        self.data_in = DataFrame()

    def set_data(self, data_in : DataFrame) -> None:
        self.data_in = data_in

    def execute(self) -> None:

        df = self.data_in.get_data()
        if self.strategy == 'average':
            self.__use_avg(df)
        elif self.strategy == 'zero':
            self.__use_zero(df)
        elif self.strategy == 'mode':
            self.__use_mode(df)

        self.data_in.set_data(df)

        self._set_output("out", self.data_in)

    def __use_avg(self, df):
        df[self.column] = df[self.column].fillna(df[self.column].mean())

    def __use_mode(self, df):
        df[self.column] = df[self.column].fillna(df[self.column].mode()[0])

    def __use_zero(self, df):
        df[self.column] = df[self.column].fillna(0)
