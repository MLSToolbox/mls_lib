""" SVMTrainer: Component that trains and makes predictions. """

from mls_lib.objects.models import SVMModel

from . sklearn_model_trainer import SKLModelTrainer
class SVMTrainer(SKLModelTrainer):
    """ SVMTrainer: Component that trains and makes predictions. """
    def __init__(self, kernel) -> None:
        super().__init__()
        self.model = SVMModel(
            kernel = kernel
        )
