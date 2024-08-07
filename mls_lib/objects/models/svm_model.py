from . model import Model
from sklearn.svm import SVR
class SVMModel(Model):
    def __init__(self, kernel):
        super().__init__()
        self.model = SVR(
            kernel = kernel
        )
    
    def train(self, features, truth):
        self.model.fit(features, truth)
    
    def predict(self, features):
        return self.model.predict(features)
    
    def score(self, x_test, y_test):
        return self.model.score(x_test, y_test)