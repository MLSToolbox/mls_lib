from .model_training_step import ModelTrainingStep
from mls_lib.objects.models import SVMModel
class SVMTrainer(ModelTrainingStep):
    def __init__(self, kernel, features, truth) -> None:
        super().__init__(
            features = features,
            truth = truth
        )
        self.model = SVMModel(
            kernel = kernel
        )
    def execute(self):
        features = self._getInput('features')
        truth = self._getInput('truth')

        self.model.train(features.getData(), truth.getData())

        self._setOutput("model", self.model)

        self.finishExecution()