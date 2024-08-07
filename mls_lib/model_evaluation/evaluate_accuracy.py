from . model_evaluation_step import ModelEvaluationStep
from sklearn import metrics
import pandas as pd
class EvaluateAccuracy(ModelEvaluationStep):
    def __init__(self, features, truth, model):
        super().__init__(
            features = features,
            truth = truth,
            model = model
        )

    def execute(self):
        model = self._getInput('model')
        x_test = self._getInput('features').getData()
        y_test = self._getInput('truth').getData()
                
        result = model.score(x_test, y_test)

        self._setOutput("result", result)

        self.finishExecution()