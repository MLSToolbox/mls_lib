""" Model prediction : Performs model prediction. """
from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task
from mls_lib.objects.models.model import Model

class ModelPredict(Task):
    """ Model prediction : Performs model prediction. """
    def __init__(self) -> None:
        super().__init__()
        self.model = Model()
        self.features = DataFrame()
        self.prediction = DataFrame()

    def set_data(self, model : Model, features : DataFrame) -> None:
        self.model = model
        self.features = features

    def execute(self):
        features = [i[0] for i in self.features.get_data().values]
        data = self.model.predict(features)

        self.prediction.from_np_array(data, self.model.get_headers())

        self._set_output("prediction", self.prediction)
