""" Accuracy evaluation step. """

from mls_lib.orchestration.task import Task
from mls_lib.objects.data_frame import DataFrame
from mls_lib.objects.models.model import Model
class EvaluateAccuracy(Task):
    """ Accuracy evaluation step. """
    def __init__(self) -> None:
        super().__init__()

        self.features = DataFrame()
        self.truth = DataFrame()
        self.model = Model()
    
    def set_data(self, features : DataFrame, truth : DataFrame, model : Model) -> None:
        """
        Sets the data for model evaluation.

        This method assigns the provided features, truth labels, and model to the
        corresponding instance variables for use in evaluating the model's accuracy.

        Parameters
        ----------
        features : DataFrame
            The input features used for model evaluation.
        truth : DataFrame
            The true labels corresponding to the input features.
        model : Model
            The model to be evaluated.

        Returns
        -------
        None
        """
        self.features = features
        self.truth = truth
        self.model = model

    def execute(self) -> None:
        """
        Execute the task.

        This method trains the model with the given features and truth labels, makes
        predictions and evaluates the accuracy of the model.

        The accuracy is then printed to the console, rounded to 2 decimal places.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        result = self.model.score(self.features.get_data(), self.truth.get_data())
        print("Accuracy: " + str(round(result*100,2)) + " %")

        self._set_output("result", result)
        