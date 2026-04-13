""" Replace Null Mode : Replaces null values of the given column with the mode of the column """

from mls_lib.orchestration import Task, Metadata
from mls_lib.objects.data_frame import DataFrame


class ReplaceNullMode(Task):
    """ Replace Null Mode : Replaces null values of the given column with the mode of the column """
    def __init__(self, column : str) -> None:
        super().__init__()
        self.column = column
        self.used_mode = None
        self.data_in = DataFrame()

    def set_data(self, data_in : DataFrame) -> None:
        self.data_in = data_in

    def execute(self) -> None:

        df = self.data_in.get_data()
        self.used_mode = df[self.column].mode()[0]
        df[self.column] = df[self.column].fillna(self.used_mode)

        self.data_in.set_data(df)

        self._set_output("out", self.data_in)

    def write_metadata(self) -> None:
        value = self.used_mode.item() if hasattr(self.used_mode, "item") else self.used_mode
        Metadata.addDataCleaningEntry(
            operation=Metadata.DataCleaningOperation.REPLACE_NULL_MODE,
            columns=[self.column],
            replacement_values=[value],
        )
