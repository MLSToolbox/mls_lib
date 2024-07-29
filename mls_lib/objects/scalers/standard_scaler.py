from . scaler import Scaler
from sklearn.preprocessing import StandardScaler

class StandardScaler(Scaler):
    def __init__(self) -> None:
        super().__init__(StandardScaler())