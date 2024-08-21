""" TrainTestSplitter: Component that trains and makes predictions. """

from sklearn.model_selection import train_test_split

from mls_lib.objects.data_frame import DataFrame

from . model_training_step import ModelTrainingStep

class SplitTrainTest(ModelTrainingStep):
    """ TrainTestSplitter: Component that trains and makes predictions. """
    def __init__(self, train_percentage : float, features, truth):
        super().__init__(
            features = features,
            truth = truth
        )
        self.train_percentage = train_percentage
    def execute(self):
        features_dataframe= self._get_input('features')
        features_data = features_dataframe.get_data()

        truth_dataframe = self._get_input('truth')
        truth_data = truth_dataframe.get_data()

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

        self.finish_execution()
