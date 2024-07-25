from . feature_engineering_step import FeatureEngineeringStep

class DataTransformer(FeatureEngineeringStep):
    def __init__(self, **origins) -> None:
        super().__init__()

        for key, value in origins:
            self.setInput(key, value)

    def execute(self):
        pass

    def transform(self):
        pass