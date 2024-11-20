""" CreateAdamsOptimizer: Component that trains and makes predictions. """

from mls_lib.objects.optimizers.adams_optimizer import AdamsOptimizer
from mls_lib.orchestration.task import Task
class CreateAdamsOptimizer(Task):
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
        self.optimizer = None
    def execute(self):
        self.optimizer = AdamsOptimizer(self.learning_rate, self.beta1, self.beta2, self.epsilon)
        self._set_output("optimizer", self.optimizer)
