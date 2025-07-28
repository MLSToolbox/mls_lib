from mls_lib.model_training import RandomForestRegressorTrainer
from mls_lib.objects.models import RandomForestRegressorModel
from pytest import fixture


@fixture
def rfrt():
    return RandomForestRegressorTrainer(
        n_estimators = 100,
        max_depth = 10,
        min_samples_leaf = 10
    )

def test_empty_rfrt(rfrt : RandomForestRegressorTrainer):
    assert rfrt is not None
    assert type(rfrt) == RandomForestRegressorTrainer
    assert rfrt.model is not None
    assert type(rfrt.model) == RandomForestRegressorModel
