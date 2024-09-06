""" SKLModelTrainer: Component that trains and makes predictions. """

from mls_lib.orchestration.step import Step
from mls_lib.objects.models import Model
from . model_training_step import ModelTrainingStep

class SKLModelTrainer(ModelTrainingStep):
    """ SKLModelTrainer: Component that trains and makes predictions. """
    def __init__(self, features : Step, truth : Step, model : Model) -> None:
        super().__init__(
            features = features,
            truth = truth
        )
        self.step_category = "model_training"
        self.model = model
    def execute(self):
        features = self._get_input('features')
        truth = self._get_input('truth')

        self.model.train(features.get_data(), truth.get_data())

        self._set_output("model", self.model)

        self._finish_execution()
