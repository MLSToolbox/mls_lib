""" SKLModelTrainer: Component that trains and makes predictions. """

from mls_lib.orchestration.task import Task
from mls_lib.objects.models import Model
from mls_lib.objects.data_frame import DataFrame
import numpy as np

class SKLModelTrainer(Task):
    """ SKLModelTrainer: Component that trains and makes predictions. """
    def __init__(self) -> None:
        super().__init__()
        self.features = DataFrame()
        self.truth = DataFrame()
        self.model = Model()
    def set_data(self, features : DataFrame, truth : DataFrame):
        """
        Sets the data for training the model.

        Parameters
        ----------
        features : DataFrame
            The input features used for training the model.
        truth : DataFrame
            The true labels corresponding to the input features.

        Returns
        -------
        None
        """
        self.features = features
        self.truth = truth

    def execute(self):
        features = self.pandasToNumpy(self.features.get_data().values)
        truth = self.pandasToNumpy(self.truth.get_data().values)
        self.model.train(
            features,
            truth
        )

        self.model.set_headers(self.truth.get_headers())

        self._set_output("model", self.model)

    def pandasToNumpy(self, values):
        if len(values[0]) == 1:
            return np.vstack([i[0] for i in values])
        return np.hstack([np.vstack([i for i in row]) for row in values]).T
