""" SVMModel: Component that trains and makes predictions. """
from sklearn.svm import SVR
from . model import Model
class SVMModel(Model):
    """ SVMModel: Component that trains and makes predictions. """
    def __init__(self, kernel):
        super().__init__()
        self.model = SVR(
            kernel = kernel
        )