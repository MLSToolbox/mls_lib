from . encoder import Encoder
from sklearn.preprocessing import LabelEncoder as LE
class LabelEncoder(Encoder):
    def __init__(self) -> None:
        super().__init__(LE())
    
    def fit_transform(self, data, columns):
        for column in columns:
            data[column] = self.encoder.fit_transform(data[column])