""" IEncoder: Component that encodes categorical data. """

from mls_lib.objects import Object
from mls_lib.objects.data_frame import DataFrame

class IEncoder(Object):
    """ IEncoder: Component that encodes categorical data. """
    def __init__(self) -> None:
        """
        Initializes the class instance with a given encoder.

        Args:
            encoder: The encoder object to be used.

        Returns:
            None
        """
        self.encoder = None
        super().__init__()

    def fit_transform(self, data, columns : list):
        """
        Fits the encoder to the data and performs a transform operation on the data.

        Parameters:
            data (numpy.ndarray): The input data to be encoded.

        Returns:
            None
        """

    def transform(self, data : DataFrame):
        """
        Transforms the input data using the encoder object.

        Parameters:
            data (object): The input data to be transformed.

        Returns:
            None
        """
