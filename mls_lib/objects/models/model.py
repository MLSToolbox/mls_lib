""" Model: Component that trains and makes predictions. """

from mls_lib.objects import Object
class Model(Object):
    """ Model: Component that trains and makes predictions. """    
    def train(self):
        """ Abstract method. """
        print("Training model...")

    def predict(self):
        """ Abstract method. """
        print("Predicting...")

    def score(self):
        """ Abstract method. """
        print("Scoring...")
