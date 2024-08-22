""" Replace Value : Replace Value Data Cleaning Step """

from mls_lib.objects.data_frame import DataFrame

from .data_cleaning_step import DataCleaningStep

class ReplaceValue(DataCleaningStep):
    """ Replace Value : Replace Value Data Cleaning Step """
    def __init__(self, column : str, value_map : dict, data_in : DataFrame) -> None:
        super().__init__(
            data_in = data_in
        )
        self.column = column
        self.value_map = value_map

    def execute(self) -> None:
        data = self._get_input("data_in").copy()
        df = data.get_data()
        df[self.column] = df[self.column].map(self.value_map)
        data.set_data(df)
        self._set_output("out", data)

        self.finish_execution()
