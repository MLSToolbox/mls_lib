""" Model: Component that trains and makes predictions. """

from mls_lib.objects import Object
from numpy import ndarray
class Model(Object):
    """ Model: Component that trains and makes predictions. """
    def __init__(self) -> None:
        super().__init__()
        self.model = None
        self.headers = None
    def train(self, features : ndarray, truth : ndarray):
        """ Train the model. """
        self.model.fit(features, truth)
    def predict(self, features : ndarray):
        """
        Makes predictions based on the given features.

        Parameters
        ----------
        features : ndarray
            The features used to make predictions.

        Returns
        -------
        numpy.ndarray
            The predictions made by the model.
        """
        return self.model.predict(features)
    def score(self, x_test : ndarray, y_test : ndarray):
        """
        Returns the mean accuracy of the model, given test data.

        Parameters
        ----------
        x_test : ndarray
            The test data to evaluate the model against.
        y_test : ndarray
            The ground truth labels for x_test.

        Returns
        -------
        float
            The mean accuracy of the model.
        """
        return self.model.score(x_test, y_test)
    def set_headers(self, headers : list[str]):
        """
        Sets the column headers for the model.

        Parameters
        ----------
        headers : list[str]
            A list of column headers.

        Returns
        -------
        None
        """
        self.headers = headers
    def get_headers(self):
        """
        Retrieves the column headers set for the model.

        Returns
        -------
        list
            A list of column headers.
        """
        return self.headers
