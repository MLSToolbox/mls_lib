""" IScaler.py """

from mls_lib.objects.object import Object
from mls_lib.objects.data_frame import DataFrame


class IScaler(Object):
    """ Abstract class that performs scaling. """

    def __init__(self):
        pass

    def fit_transform(self, data : DataFrame, columns : list):
        """
        Fits the scaler to the data and performs a transform operation on the specified column.

        Parameters:
            data (numpy.ndarray): The input data to be scaled.

        Returns:
            None
        """
        pass

    def transform(self, data : DataFrame):
        """
        Transforms the specified column of the input data using the scaler object.

        Parameters:
            data (numpy.ndarray): The input data to be scaled.

        Returns:
            None
        """
        pass
    