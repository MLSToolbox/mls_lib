""" Accuracy evaluation step. """

from mls_lib.orchestration.step import Step
from . model_evaluation_step import ModelEvaluationStep

class EvaluateAccuracy(ModelEvaluationStep):
    """ Accuracy evaluation step. """
    def __init__(self, features : Step, truth : Step, model : Step) -> None:
        super().__init__(
            features = features,
            truth = truth,
            model = model
        )

    def execute(self) -> None:
        model = self._get_input('model')
        x_test = self._get_input('features').get_data()
        y_test = self._get_input('truth').get_data()

        result = model.score(x_test, y_test)

        self._set_output("result", result)

        self._finish_execution()
        