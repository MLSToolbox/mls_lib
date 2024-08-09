""" RobustScaler: Component that performs robust scaling. """

from sklearn.preprocessing import RobustScaler as RS

from . scaler import Scaler

class RobustScaler(Scaler):
    """ RobustScaler: Component that performs robust scaling. """
    def __init__(self) -> None:
        super().__init__(RS())
        