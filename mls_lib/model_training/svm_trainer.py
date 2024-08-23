""" SVMTrainer: Component that trains and makes predictions. """

from mls_lib.objects.models import SVMModel

from . model_training_step import ModelTrainingStep
class SVMTrainer(ModelTrainingStep):
    """ SVMTrainer: Component that trains and makes predictions. """
    def __init__(self, kernel, features, truth) -> None:
        super().__init__(
            features = features,
            truth = truth,
            model = SVMModel(
                kernel = kernel
            )
        )
        