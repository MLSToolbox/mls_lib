""" Join: Component that joins two tables. """
from mls_lib.orchestration import Step
from mls_lib.objects.data_frame import DataFrame
from . feature_engineering_step import FeatureEngineeringStep

class Join(FeatureEngineeringStep):
    """ Join: Component that joins two tables. """
    def __init__(self, left : Step, right : Step, how : str, index : list) -> None:
        super().__init__(
            left = left,
            right = right,
        )

        self.index = index
        self.how = how

    def execute(self):

        left = self._get_input("left")
        right = self._get_input("right")

        df = left.get_data()
        df = df.join(right.get_data(), on = self.index, how = self.how)

        new_df = DataFrame()
        new_df.set_data(df)
        self._set_output("out", new_df)

        self._finish_execution()
