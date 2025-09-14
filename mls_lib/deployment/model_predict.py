""" Model prediction : Performs model prediction. """
from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task
from mls_lib.objects.models.model import Model
import numpy as np

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
        features = self.pandasToNumpy(self.features.get_data().values)
        data = self.model.predict(features)

        self.prediction.from_np_array(data, self.model.get_headers())

        self._set_output("prediction", self.prediction)

    def pandasToNumpy(self, values):
        if len(values[0]) == 1:
            return np.vstack([i[0] for i in values])
        return np.hstack([np.vstack([i for i in row]) for row in values]).T
