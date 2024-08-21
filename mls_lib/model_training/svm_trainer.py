""" SVMTrainer: Component that trains and makes predictions. """

from mls_lib.objects.models import SVMModel

from .model_training_step import ModelTrainingStep
class SVMTrainer(ModelTrainingStep):
    """ SVMTrainer: Component that trains and makes predictions. """
    def __init__(self, kernel, features, truth) -> None:
        super().__init__(
            features = features,
            truth = truth
        )
        self.model = SVMModel(
            kernel = kernel
        )
    def execute(self):
        features = self._get_input('features')
        truth = self._get_input('truth')

        self.model.train(features.get_data(), truth.get_data())

        self._set_output("model", self.model)

        self.finish_execution()
        