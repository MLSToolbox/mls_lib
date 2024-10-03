""" TrainTestSplitter: Component that trains and makes predictions. """

from sklearn.model_selection import train_test_split

from mls_lib.orchestration.task import Task
from mls_lib.objects.data_frame import DataFrame

class TrainTestSplitter(Task):
    """ TrainTestSplitter: Component that trains and makes predictions. """
    def __init__(self, train_percentage : float):
        super().__init__()
        self.features = DataFrame()
        self.truth = DataFrame()
        self.train_percentage = train_percentage
    
    def set_data(self, features : DataFrame, truth : DataFrame) -> None:
        self.features = features
        self.truth = truth

    def execute(self):
        features_data = self.features.get_data()
        truth_data = self.truth.get_data()

        x_train, x_test, y_train, y_test = train_test_split(
            features_data,
            truth_data,
            train_size = self.train_percentage)

        x_train_dataframe, y_train_dataframe = [DataFrame(), DataFrame(),]
        x_test_dataframe, y_test_dataframe = [DataFrame(), DataFrame()]

        x_train_dataframe.set_data(x_train)
        y_train_dataframe.set_data(y_train)
        x_test_dataframe.set_data(x_test)
        y_test_dataframe.set_data(y_test)

        self._set_output("features_train", x_train_dataframe)
        self._set_output("truth_train", y_train_dataframe)
        self._set_output("features_test", x_test_dataframe)
        self._set_output("truth_test", y_test_dataframe)
