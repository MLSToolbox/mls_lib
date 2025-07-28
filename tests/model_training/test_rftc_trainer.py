from mls_lib.model_training import RandomForestTreeClassifierTrainer
from mls_lib.objects.models import RandomForestClassifierModel
from pytest import fixture


@fixture
def rftct():
    return RandomForestTreeClassifierTrainer(
        n_estimators = 100,
        max_depth = 10
    )

def test_empty_rfrt(rftct : RandomForestTreeClassifierTrainer):
    assert rftct is not None
    assert type(rftct) == RandomForestTreeClassifierTrainer
    assert rftct.model is not None
    assert type(rftct.model) == RandomForestClassifierModel
