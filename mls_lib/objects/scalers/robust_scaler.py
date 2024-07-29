from . scaler import Scaler
from sklearn.preprocessing import RobustScaler

class RobustScaler(Scaler):
    def __init__(self) -> None:
        super().__init__(RobustScaler())