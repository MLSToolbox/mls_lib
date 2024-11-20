""" RandomForestRegressorModel: Component that trains and makes predictions. """
from sklearn.ensemble import RandomForestRegressor as RFR
from .model import Model
class RandomForestRegressorModel(Model):
    """ RandomForestRegressorModel: Component that trains and makes predictions. """
    def __init__(self, n_estimators, max_depth, min_samples_leaf):
        super().__init__()
        self.model = RFR(
            n_estimators = int(n_estimators),
            max_depth = int(max_depth),
            min_samples_leaf = int(min_samples_leaf)
        )
    def train(self, features = None, truth = None):
        """ Train the model. """
        self.model.fit(features, truth)
