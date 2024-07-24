from mls_lib.model_training.optimizers import OptimizerStep

class Adam(OptimizerStep):
    def __init__(self, parameters : str) -> None:
        self.parameters = parameters
        super().__init__()
