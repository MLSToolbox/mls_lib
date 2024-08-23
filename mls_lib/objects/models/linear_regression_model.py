""" LinearRegressionModel: Component that trains and makes predictions. """
from sklearn.linear_model import LinearRegression
from . model import Model
class LinearRegressionModel(Model):
    """ LinearRegressionModel: Component that trains and makes predictions. """
    def __init__(self):
        super().__init__(
            model = LinearRegression()
        )
        