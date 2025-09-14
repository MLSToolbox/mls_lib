""" Clssification Report Generator. """
from .evaluate_accuracy import EvaluateAccuracy

class EvaluateClassificationReport(EvaluateAccuracy):
    """ Clssification Report Generator. """
    def __init__(self) -> None:
        super().__init__()
    def execute(self) -> None:
        """
        Execute the task.

        This method generates a classification report for the model.

        The classification report is then printed to the console.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        features = self.pandasToNumpy(self.features.get_data().values)
        truth = self.pandasToNumpy(self.truth.get_data().values)

        result = self.model.classificationReport(features, truth)
        print("Classification Report:\n", result)

        self._set_output("report", result)
