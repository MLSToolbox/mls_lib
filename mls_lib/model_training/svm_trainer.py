from .model_training_step import ModelTrainingStep
from mls_lib.objects.models import SVMModel
class SVMTrainer(ModelTrainingStep):
    def __init__(self, model_parameters, optimizer, features, truth) -> None:
        super().__init__(
            optimizer = optimizer,
            features = features,
            truth = truth
        )
        self.model_parameters = model_parameters
    def execute(self):
        model = SVMModel()

        #model.train(self.model_parameters)
        
        self._setOutput("model", model)

        self.finishExecution()