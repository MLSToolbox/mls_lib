""""""

from mls_lib.objects.models import LinearRegressionModel

from .model_training_step import ModelTrainingStep
class LinearRegressionTrainer(ModelTrainingStep):
    """"""
    def __init__(self, features, truth) -> None:
        super().__init__(
            features = features,
            truth = truth,
            model = LinearRegressionModel()
        )
        