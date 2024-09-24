""" Join: Component that joins two tables. """
from mls_lib.orchestration import Step
from mls_lib.objects.data_frame import DataFrame

class Join(Step):
    """ Join: Component that joins two tables. """
    def __init__(self, how : str, index : list) -> None:
        super().__init__(
        )
        self.left = DataFrame()
        self.right = DataFrame()
        self.index = index
        self.how = how

    def set_data(self, left : DataFrame, right : DataFrame) -> None:
        self.left = left
        self.right = right
    def execute(self):
        df = self.left.get_data()
        df = df.join(self.right.get_data(), on = self.index, how = self.how)

        new_df = DataFrame()
        new_df.set_data(df)
        self._set_output("out", new_df)
