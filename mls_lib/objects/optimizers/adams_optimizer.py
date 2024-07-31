from mls_lib.objects.object import Object
class AdamsOptimizer(Object):
    def __init__(self, learning_rate, beta1, beta2, epsilon) -> None:
        super().__init__()
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        