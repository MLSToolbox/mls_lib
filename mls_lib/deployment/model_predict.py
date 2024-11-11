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
        self.predictions = DataFrame()
    
    def set_data(self, model : Model, features : DataFrame) -> None:
        self.model = model
        self.features = features
    
    def execute(self):
        data = self.model.predict(self.features.get_data())
        
        self.predictions.set_data(data)

        self._set_output("predictions", self.predictions)