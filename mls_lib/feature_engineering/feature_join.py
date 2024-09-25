""" Join: Component that joins two tables. """
from mls_lib.orchestration import Step
from mls_lib.objects.data_frame import DataFrame
import pandas as pd

class FeatureJoin(Step):
    """ Join: Component that joins two tables. """
    def __init__(self) -> None:
        super().__init__(
        )
        self.left = DataFrame()
        self.right = DataFrame()

    def set_data(self, left : DataFrame, right : DataFrame) -> None:
        self.left = left
        self.right = right
    def execute(self):
        df_left =  self.left.get_data()
        df_right = self.right.get_data()
        
        df = pd.concat([df_left, df_right], axis = 1)

        new_df = DataFrame()
        new_df.set_data(df)
        
        self._set_output("out", new_df)
