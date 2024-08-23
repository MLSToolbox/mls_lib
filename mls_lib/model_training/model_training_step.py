""" Model Training Step """

from mls_lib.orchestration import Step

from mls_lib.objects.data_frame import DataFrame
from mls_lib.objects.models.model import Model

class ModelTrainingStep(Step):
    """ Model Training Step """
    def __init__(self, features : DataFrame, truth : DataFrame, model : Model) -> None:
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