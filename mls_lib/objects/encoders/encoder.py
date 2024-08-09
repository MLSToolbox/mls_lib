""" Encoder: Component that encodes categorical data. """
from mls_lib.objects import Object

class Encoder(Object):
    """ Encoder: Component that encodes categorical data. """
    def __init__(self, encoder) -> None:
        """
        Initializes the class instance with a given encoder.

        Args:
            encoder: The encoder object to be used.

        Returns:
            None
        """
        super().__init__()
        self.encoder = encoder

    def fit_transform(self, data, columns):
        """
        Fits the encoder to the data and performs a transform operation on the data.

        Parameters:
            data (numpy.ndarray): The input data to be encoded.

        Returns:
            None
        """
        self.encoder.fit_transform(data[columns])

    def transform(self, data):
        """
        Transforms the input data using the encoder object.

        Parameters:
            data (object): The input data to be transformed.

        Returns:
            None
        """
        data.data = self.encoder.transform(data.data)
