""" CreateAdamsOptimizer: Component that trains and makes predictions. """

from mls_lib.objects.optimizers.adams_optimizer import AdamsOptimizer

from . model_training_step import ModelTrainingStep

class CreateAdamsOptimizer(ModelTrainingStep):
    """ CreateAdamsOptimizer: Component that trains and makes predictions. """
    def __init__(self, optimizer_parameters = None): #learning_rate, beta1, beta2, epsilon) -> None:
        super().__init__()
        # self.learning_rate = learning_rate
        # self.beta1 = beta1
        # self.beta2 = beta2
        # self.epsilon = epsilon

        self.learning_rate = 0.0
        self.beta1 = 0.0
        self.beta2 = 0.0
        self.epsilon = 0.0
        self.optimizer_parameters = optimizer_parameters
    def execute(self):
        self._set_output("optimizer",
                         AdamsOptimizer(self.learning_rate, self.beta1, self.beta2, self.epsilon))
        self._finish_execution()
