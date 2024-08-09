""" Feature Engineering Step """
from mls_lib.orchestration import Step

class FeatureEngineeringStep(Step):
    """ Feature Engineering Step """
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        self.step_category = "feature_engineering"
