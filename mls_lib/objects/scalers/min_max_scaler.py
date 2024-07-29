from . scaler import Scaler
from sklearn.preprocessing import MinMaxScaler

class MinMaxScaler(Scaler):
    def __init__(self) -> None:
        super().__init__(MinMaxScaler())