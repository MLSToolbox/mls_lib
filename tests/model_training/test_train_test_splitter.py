from mls_lib.model_training import TrainTestSplitter
from mls_lib.objects.data_frame import DataFrame
def test_train_test_splitter():
    train_test_splitter = TrainTestSplitter(0.8)
    assert train_test_splitter.train_percentage == 0.8

def test_set_data():
    train_test_splitter = TrainTestSplitter(0.8)
    features = DataFrame()
    truth = DataFrame()
    train_test_splitter.set_data(features, truth)
    assert train_test_splitter.features == features
    assert train_test_splitter.truth == truth

def test_execute():

    train_test_splitter = TrainTestSplitter(0.8)
    features = DataFrame()
    features.from_np_array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['a'])
    truth = DataFrame()
    truth.from_np_array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['a'])
    train_test_splitter.set_data(features, truth)
    train_test_splitter.execute()
    assert train_test_splitter.get_output("features_train") is not None
    assert train_test_splitter.get_output("truth_train") is not None
    assert train_test_splitter.get_output("features_test") is not None
    assert train_test_splitter.get_output("truth_test") is not None
    assert len(train_test_splitter.get_output("features_train").get_data()) == 8
    assert len(train_test_splitter.get_output("truth_train").get_data()) == 8
    assert len(train_test_splitter.get_output("features_test").get_data()) == 2
    assert len(train_test_splitter.get_output("truth_test").get_data()) == 2