""" StandardScaler: Component that performs standard scaling. """

from sklearn.preprocessing import StandardScaler as SS

from . scaler import Scaler

class StandardScaler(Scaler):
    """ StandardScaler: Component that performs standard scaling. """
    def __init__(self) -> None:
        super().__init__(SS())
