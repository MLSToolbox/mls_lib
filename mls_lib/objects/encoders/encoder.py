""" Encoder: Component that encodes categorical data. """

from mls_lib.objects.encoders.iencoder import IEncoder
from mls_lib.objects.data_frame import DataFrame

class Encoder(IEncoder):
    """ Encoder: Component that encodes categorical data. """
    def __init__(self, encoder : IEncoder) -> None:
        """
        Initializes the class instance with a given encoder.

        Args:
            encoder: The encoder object to be used.

        Returns:
            None
        """
        super().__init__()
        self.encoder = encoder
        self.columns = []

    def fit_transform(self, data : DataFrame, columns : list):
        """
        Fits the encoder to the data and performs a transform operation on the data.

        Parameters:
            data (numpy.ndarray): The input data to be encoded.

        Returns:
            None
        """
        self.columns = columns
        return self.encoder.fit_transform(data, self.columns)
    def transform(self, data):
        """
        Transforms the input data using the encoder object.

        Parameters:
            data (object): The input data to be transformed.

        Returns:
            None
        """
        return self.encoder.transform(data, self.columns)
        