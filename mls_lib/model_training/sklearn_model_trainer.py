""" SKLModelTrainer: Component that trains and makes predictions. """

from mls_lib.orchestration.task import Task
from mls_lib.objects.models import Model
from mls_lib.objects.data_frame import DataFrame

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
        self.model.train(self.features.get_data(), self.truth.get_data())

        self.model.set_headers(self.truth.get_headers())

        self._set_output("model", self.model)
