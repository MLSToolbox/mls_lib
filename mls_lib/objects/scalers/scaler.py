""" Scaler: Component that performs scaling. """

import numpy as np

from mls_lib.objects.data_frame import DataFrame

from .iscaler import IScaler

class Scaler(IScaler):
    """ Scaler: Component that performs scaling. """
    def __init__(self, scaler : IScaler) -> None:
        """
        Initializes the class instance with a given scaler and column.

        Args:
            scaler (object): The scaler object to be used for scaling the data.
            columns (list): A list containing the column name(s) to be scaled.

        Returns:
            None
        """
        super().__init__()
        self.scaler = scaler
        self.columns = []

    def fit_transform(self, data : DataFrame, columns : list):
        """
        Fits the scaler to the data and performs a transform operation on the specified column.

        Parameters:
            data (numpy.ndarray): The input data to be scaled.

        Returns:
            None
        """
        self.columns = columns
        df = data.get_data()
        df[self.columns] = self.scaler.fit_transform(df[self.columns].values)
        data.set_data(df)

    def transform(self, data : DataFrame):
        """
        Transforms the specified column of the input data using the scaler object.

        Parameters:
            data (object): The input data to be transformed.

        Returns:
            None

        """
        df = data.get_data()
        df[self.columns] = self.scaler.transform(np.array(df[self.columns]).reshape(-1,1))
        data.set_data(df)