""" OneHotEncoder: Component that trains a one hot encoder. """

from category_encoders import OneHotEncoder as OHE
from mls_lib.objects.data_frame import DataFrame

from . encoder import Encoder

class OneHotEncoder(Encoder):
    """ OneHotEncoder: Component that trains a one hot encoder. """
    def __init__(self, cols) -> None:
        self.encoder = OHE(cols=cols)
        self.columns = cols


    def fit_transform(self, data : DataFrame, columns : list):
        """
        Fits the encoder to the data and performs a transform operation on the data.

        Parameters:
            data (numpy.ndarray): The input data to be encoded.

        Returns:
            None
        """
        self.encoder.fit(data)
        return self.encoder.transform(data, True)
    def transform(self, data):
        """
        Transforms the input data using the encoder object.

        Parameters:
            data (object): The input data to be transformed.

        Returns:
            None
        """
        return self.encoder.transform(data, True)