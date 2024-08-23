""" IScaler.py """

from mls_lib.objects.object import Object
from mls_lib.objects.data_frame import DataFrame


class IScaler(Object):
    """ Abstract class that performs scaling. """

    def __init__(self):
        """
        Initializes the class instance with a given scaler and column.

        Args:
            scaler (object): The scaler object to be used for scaling the data.
            columns (list): A list containing the column name(s) to be scaled.

        Returns:
            None
        """
        self.scaler = None
        super().__init__()

    def fit_transform(self, data : DataFrame, columns : list):
        """
        Fits the scaler to the data and performs a transform operation on the specified column.

        Parameters:
            data (numpy.ndarray): The input data to be scaled.

        Returns:
            None
        """

    def transform(self, data : DataFrame):
        """
        Transforms the specified column of the input data using the scaler object.

        Parameters:
            data (numpy.ndarray): The input data to be scaled.

        Returns:
            None
        """
