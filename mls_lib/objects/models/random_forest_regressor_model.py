""" RandomForestRegressorModel: Component that trains and makes predictions. """
from sklearn.ensemble import RandomForestClassifier as RFC
from .model import Model
class RandomForestRegressorModel(Model):
    """ RandomForestRegressorModel: Component that trains and makes predictions. """
    def __init__(self, n_estimators, max_depth, min_samples_leaf):
        super().__init__()
        self.model = RFC(
            n_estimators = n_estimators,
            max_depth = max_depth,
            min_samples_leaf = min_samples_leaf
        )