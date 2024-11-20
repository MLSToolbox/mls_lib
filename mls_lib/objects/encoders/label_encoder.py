""" LabelEncoder: Component that encodes categorical data. """
from sklearn.preprocessing import LabelEncoder as LE

from . encoder import Encoder

class LabelEncoder(Encoder):
    """ LabelEncoder: Component that encodes categorical data. """
    def __init__(self) -> None:
        super().__init__(LE())
    def fit_transform(self, data, columns : list):
        self.columns = columns
        for column in columns:
            data[column] = self.encoder.fit_transform(data[column])
    def transform(self, data):
        for column in self.columns:
            data[column] = self.encoder.transform(data[column])
