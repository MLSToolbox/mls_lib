""" MSE evaluation step. """
from .evaluate_accuracy import EvaluateAccuracy

class EvaluateMSE(EvaluateAccuracy):
    """ MSE evaluation step. """
    def __init__(self) -> None:
        super().__init__()
    def execute(self) -> None:
        """
        Execute the task.

        This method evaluates the MSE of the model.

        The MSE is then printed to the console, rounded to 2 decimal places.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        features = self.pandasToNumpy(self.features.get_data().values)
        truth = self.pandasToNumpy(self.truth.get_data().values)

        mse = self.model.scoreMSE(features, truth)
        rmse = self.model.scoreRMSE(features, truth)
        print("MSE: " + str(round(mse*100,2)) + " %")
        print("RMSE: " + str(round(rmse*100,2)) + " %")

        self._set_output("MSE", mse)
        self._set_output("RMSE", rmse)
