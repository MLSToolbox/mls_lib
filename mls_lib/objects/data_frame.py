""" DataFrame: Component that holds data. """

from .object import Object
import pandas as pd
class DataFrame(Object):
    """ DataFrame: Component that holds data. """
    def __init__(self):
        self.data = None
    def get_data(self) -> pd.DataFrame:
        """ Returns the data. """
        return self.data

    def set_data(self, data):
        """ Sets the data. """
        self.data = data
