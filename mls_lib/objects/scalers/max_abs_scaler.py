from . scaler import Scaler
from sklearn.preprocessing import MaxAbsScaler

class MaxAbsScaler(Scaler):
    def __init__(self) -> None:
        super().__init__(MaxAbsScaler())