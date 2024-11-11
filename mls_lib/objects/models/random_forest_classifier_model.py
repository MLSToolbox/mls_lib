""" RandomForestClassifierModel: Component that trains and makes predictions. """
from sklearn.ensemble import RandomForestClassifier as RFC
from . model import Model
class RandomForestClassifierModel(Model):
    """ RandomForestClassifierModel: Component that trains and makes predictions. """
    def __init__(self, max_depth = None, n_estimators = 100) -> None:
        super().__init__()
        self.model = RFC(
            max_depth = int(max_depth),
            n_estimators = int(n_estimators)
        )
    