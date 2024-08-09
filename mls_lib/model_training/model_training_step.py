""" Model Training Step """
from mls_lib.orchestration import Step

class ModelTrainingStep(Step):
    """ Model Training Step """
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        self.step_category = "model_training"
        