""" LinearRegressionTrainer: Component that trains and makes predictions. """

from mls_lib.objects.models import RandomForestClassifierModel

from . sklearn_model_trainer import SKLModelTrainer
class RandomForestTreeClassifierTrainer(SKLModelTrainer):
    """ LinearRegressionTrainer: Component that trains and makes predictions. """
    def __init__(self, features, truth, max_depth = None, n_estimators = 100) -> None:
        super().__init__(
            features = features,
            truth = truth,
            model = RandomForestClassifierModel(
                max_depth = max_depth,
                n_estimators = n_estimators
            )
        )
        