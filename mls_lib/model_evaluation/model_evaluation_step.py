""" Model Evaluation Step """
from mls_lib.orchestration import Step

class ModelEvaluationStep(Step):
    """ Model Evaluation Step """
    def __init__(self, **inputs):
        super().__init__(**inputs)
        self.step_category = "model_evaluation"
