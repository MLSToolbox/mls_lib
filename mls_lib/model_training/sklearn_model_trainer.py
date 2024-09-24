""" SKLModelTrainer: Component that trains and makes predictions. """

from mls_lib.orchestration.step import Step
from mls_lib.objects.models import Model
from mls_lib.objects.data_frame import DataFrame

class SKLModelTrainer(Step):
    """ SKLModelTrainer: Component that trains and makes predictions. """
    def __init__(self) -> None:
        super().__init__()
        self.features = DataFrame()
        self.truth = DataFrame()
        self.model = Model()
    def set_data(self, features : DataFrame, truth : DataFrame):
        self.features = features
        self.truth = truth
    def execute(self):
        self.model.train(self.features.get_data(), self.truth.get_data())

        self._set_output("model", self.model)