""" Data Collection Step """

from mls_lib.orchestration import Step

class DataCollectionStep(Step):
    """ Data Collection Step """

    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        self.step_category = "data_collection"
        