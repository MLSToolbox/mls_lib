""" MaxAbsScaler: Component that performs max abs scaling. """

from sklearn.preprocessing import MaxAbsScaler as MAS

from . scaler import Scaler

class MaxAbsScaler(Scaler):
    """ MaxAbsScaler: Component that performs max abs scaling. """
    def __init__(self) -> None:
        super().__init__(MAS())
