from . model_training_step import ModelTrainingStep
from sklearn.model_selection import train_test_split
from mls_lib.objects.data_frame import DataFrame

class SplitTrainTest(ModelTrainingStep):
    def __init__(self, train_percentage : float, features, truth):
        super().__init__(
            features = features,
            truth = truth
        )
        self.train_percentage = train_percentage
        
    def execute(self):
        features_dataframe= self._getInput('features')
        features_data = features_dataframe.getData()

        truth_dataframe = self._getInput('truth')
        truth_data = truth_dataframe.getData()

        x_train, x_test, y_train, y_test = train_test_split(features_data, truth_data, train_size = self.train_percentage)

        x_train_dataframe, y_train_dataframe, x_test_dataframe, y_test_dataframe = [DataFrame(), DataFrame(), DataFrame(), DataFrame()]

        x_train_dataframe.setData(x_train)
        y_train_dataframe.setData(y_train)
        x_test_dataframe.setData(x_test)
        y_test_dataframe.setData(y_test)

        self._setOutput("features_train", x_train_dataframe)
        self._setOutput("truth_train", y_train_dataframe)
        self._setOutput("features_test", x_test_dataframe)
        self._setOutput("truth_test", y_test_dataframe)

        self.finishExecution()