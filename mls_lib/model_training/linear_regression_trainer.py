""" LinearRegressionTrainer: Component that trains and makes predictions. """

from mls_lib.objects.models import LinearRegressionModel

from . sklearn_model_trainer import SKLModelTrainer
class LinearRegressionTrainer(SKLModelTrainer):
    """ LinearRegressionTrainer: Component that trains and makes predictions. """
    def __init__(self, features, truth) -> None:
        super().__init__(
            features = features,
            truth = truth,
            model = LinearRegressionModel()
        )
        