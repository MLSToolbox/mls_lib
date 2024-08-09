""" AdamsOptimizer: Component that trains and makes predictions. """

from mls_lib.objects.object import Object

class AdamsOptimizer(Object):
    """ AdamsOptimizer: Component that trains and makes predictions. """
    def __init__(self, learning_rate, beta1, beta2, epsilon) -> None:
        super().__init__()
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
    def get_params(self):
        """ Returns the parameters of the optimizer. """
        return {
            "learning_rate": self.learning_rate,
            "beta1": self.beta1,
            "beta2": self.beta2,
            "epsilon": self.epsilon
        }
        