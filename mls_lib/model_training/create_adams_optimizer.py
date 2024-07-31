from . model_training_step import ModelTrainingStep
from mls_lib.objects.optimizers.adams_optimizer import AdamsOptimizer
class CreateAdamsOptimizer(ModelTrainingStep):

    def __init__(self, optimizer_parameters): #learning_rate, beta1, beta2, epsilon) -> None:
        super().__init__()
        """
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        """
        self.learning_rate = 0.0
        self.beta1 = 0.0
        self.beta2 = 0.0
        self.epsilon = 0.0

    def execute(self):
        self._setOutput("optimizer",
                         AdamsOptimizer(self.learning_rate, self.beta1, self.beta2, self.epsilon))
        
        self.finishExecution()