""" SVMModel: Component that trains and makes predictions. """
from sklearn.ensemble import RandomForestClassifier
from . model import Model
class RandomForestClassifierModel(Model):
    """ SVMModel: Component that trains and makes predictions. """
    def __init__(self, max_depth = None, n_estimators = 100) -> None:
        super().__init__(
            model = RandomForestClassifier(
                max_depth = max_depth,
                n_estimators = n_estimators
            )
        )
    