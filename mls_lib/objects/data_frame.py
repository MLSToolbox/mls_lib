""" DataFrame: Component that holds data. """
from copy import deepcopy
import pandas as pd
from .object import Object
import numpy
class DataFrame(Object):
    """ DataFrame: Component that holds data. """
    def __init__(self):
        self.data = None
    def get_data(self) -> pd.DataFrame:
        """
        Returns a deep copy of the data stored in the DataFrame object.

        Returns
        -------
        pandas.DataFrame
            A deep copy of the data stored in the object.
        """
        return deepcopy(self.data)

    def set_data(self, data : pd.DataFrame):
        """
        Sets the data for the DataFrame object.

        Parameters
        ----------
        data : pandas.DataFrame
            The DataFrame to be stored in the object. A deep copy of this data is made.

        Returns
        -------
        None
        """
        self.data = deepcopy(data)

    def from_np_array(self, data : numpy.ndarray, headers : list[str]):
        """
        Creates a DataFrame from a numpy array.

        Parameters
        ----------
        data : numpy.ndarray
            The numpy array to be converted to a DataFrame.

        Returns
        -------
        None

        """
        self.data = pd.DataFrame( data, columns = headers)
    
    def get_headers(self):
        """
        Retrieves the column headers of the DataFrame.

        Returns
        -------
        list
            A list of column headers in the DataFrame.
        """
        return self.data.columns.tolist()
    def set_headers(self, headers : list[str]):
        """
        Sets the column headers for the DataFrame.

        Parameters
        ----------
        headers : list[str]
            A list of column headers.

        Returns
        -------
        None
        """
        self.data.columns = headers
