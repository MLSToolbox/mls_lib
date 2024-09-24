""" Model: Component that trains and makes predictions. """

from mls_lib.objects import Object
class Model(Object):

    def __init__(self) -> None:
        super().__init__()
        self.model = None

    """ Model: Component that trains and makes predictions. """
    def train(self, features = None, truth = None):
        """ Train the model. """
        self.model.fit(features, truth)
    def predict(self, features = None):
        """ Make predictions. """
        return self.model.predict(features)
    def score(self, x_test = None, y_test = None):
        """ Score the model. """
        return self.model.score(x_test, y_test)
