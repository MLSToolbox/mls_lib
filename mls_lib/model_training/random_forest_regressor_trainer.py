""" RandomForestRegressorTrainer: Component that trains and makes predictions. """

from mls_lib.objects.models import RandomForestRegressorModel

from . sklearn_model_trainer import SKLModelTrainer
class RandomForestRegressorTrainer(SKLModelTrainer):
    """ RandomForestRegressorTrainer: Component that trains and makes predictions. """
    def __init__(self, n_estimators, max_depth, min_samples_leaf) -> None:
        super().__init__()

        self.model = RandomForestRegressorModel(n_estimators, max_depth, min_samples_leaf)
        