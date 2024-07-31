from . model_evaluation_step import ModelEvaluationStep

class Evaluate(ModelEvaluationStep):
    def __init__(self, parameters, model, features, truth):
        super().__init__(
            model = model,
            features = features,
            truth = truth,
        )
        self.model = parameters
    
    def execute(self):
        model = self._getInput('model')
        x_test = self._getInput('features')
        y_test = self._getInput('truth')

        # result = model.evaluate(x_test, y_test)
        result = None

        self._setOutput("result", result)
        
        self.finishExecution()