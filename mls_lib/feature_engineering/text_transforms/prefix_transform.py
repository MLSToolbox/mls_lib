""" PrefixTransform: """

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task

class PrefixTransform(Task):
    """"""
    def __init__(self, columns : list[str], prefix_length : int) -> None:
        super().__init__()
        self.old_table = DataFrame()
        self.columns = columns
        self.prefix_length = prefix_length

    def set_data(self, old_table : DataFrame) -> None:
        self.old_table = old_table

    def execute(self) -> None:
        data = self.old_table.get_data()
        for column in self.columns:
            data[column] = data[column].apply(lambda x: x[:self.prefix_length])
        
        new_df = DataFrame()
        new_df.set_data(data)

        self._set_output("new_table", new_df)
