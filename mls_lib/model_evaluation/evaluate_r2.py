""" R2 evaluation step. """
from .evaluate_accuracy import EvaluateAccuracy

class EvaluateR2(EvaluateAccuracy):
    """ R2 evaluation step. """
    def __init__(self) -> None:
        super().__init__()
    def execute(self) -> None:
        """
        Execute the task.

        This method evaluates the R2 of the model.

        The R2 is then printed to the console, rounded to 2 decimal places.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        result = self.model.scoreR2(self.features.get_data(), self.truth.get_data())
        print("R2: " + str(round(result*100,2)) + " %")

        self._set_output("r2", result)
