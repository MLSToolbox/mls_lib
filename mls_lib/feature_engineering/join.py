""" Join: Component that joins two tables. """
from . feature_engineering_step import FeatureEngineeringStep

class Join(FeatureEngineeringStep):
    """ Join: Component that joins two tables. """
    def __init__(self, left, right, on, how):
        super().__init__(
            left = left,
            right = right,
        )
        self.on = on
        self.how = how

    def execute(self):
        self.finish_execution()
