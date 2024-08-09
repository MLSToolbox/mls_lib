""" Data Cleaning Step """
from mls_lib.orchestration import Step

class DataCleaningStep(Step):
    """ Data Cleaning Step """
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        self.step_category = "data_cleaning"
