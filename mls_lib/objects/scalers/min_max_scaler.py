""" MinMaxScaler: Component that performs min max scaling. """

from sklearn.preprocessing import MinMaxScaler as  MMS

from . scaler import Scaler

class MinMaxScaler(Scaler):
    """ MinMaxScaler: Component that performs min max scaling. """
    def __init__(self) -> None:
        super().__init__(MMS())
