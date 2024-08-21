""" Accuracy evaluation step. """
from . model_evaluation_step import ModelEvaluationStep

class EvaluateAccuracy(ModelEvaluationStep):
    """ Accuracy evaluation step. """
    def __init__(self, features, truth, model):
        super().__init__(
            features = features,
            truth = truth,
            model = model
        )

    def execute(self):
        model = self._get_input('model')
        x_test = self._get_input('features').get_data()
        y_test = self._get_input('truth').get_data()

        result = model.score(x_test, y_test)

        self._set_output("result", result)

        self.finish_execution()
        