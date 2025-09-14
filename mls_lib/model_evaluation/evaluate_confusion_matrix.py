""" Confusion Matrix evaluation step. """
from .evaluate_accuracy import EvaluateAccuracy

class EvaluateConfusionMatrix(EvaluateAccuracy):
    """ Confusion Matrix evaluation step. """
    def __init__(self) -> None:
        super().__init__()
    def execute(self) -> None:
        """
        Execute the task.

        This method generates a confusion matrix for the model.

        The confusion matrix is then printed to the console.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        features = self.pandasToNumpy(self.features.get_data().values)
        truth = self.pandasToNumpy(self.truth.get_data().values)

        result = self.model.confusionMatrix(features, truth)
        print("Confusion Matrix:\n", result)

        self._set_output("confusion_matrix", result)
