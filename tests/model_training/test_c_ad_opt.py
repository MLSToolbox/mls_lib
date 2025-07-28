from mls_lib.model_training import CreateAdamsOptimizer
from pytest import fixture


@fixture
def cao():
    return CreateAdamsOptimizer()

def test_empty_cao(cao : CreateAdamsOptimizer):
    assert cao is not None
    assert cao.beta1 == 0.0
    assert cao.beta2 == 0.0
    assert cao.epsilon == 0.0
    assert cao.learning_rate == 0.0
    assert cao.optimizer is None
    assert cao.optimizer_parameters is None

def test_filled_cao():
    cao = CreateAdamsOptimizer( optimizer_parameters= [1.0, 2.0, 3.0, 4.0] )
    assert cao.optimizer_parameters == [1.0, 2.0, 3.0, 4.0]

def test_execute_cao(cao : CreateAdamsOptimizer):
    cao.execute()
    assert cao.get_output("optimizer") is not None
    resulting_opt = cao.get_output("optimizer")
    assert resulting_opt.learning_rate == 0.0
    assert resulting_opt.beta1 == 0.0
    assert resulting_opt.beta2 == 0.0
    assert resulting_opt.epsilon == 0.0

