from ....mls_lib.objects.optimizers import AdamsOptimizer

def test_adams_optimizer():
    a = AdamsOptimizer(
        learning_rate=0.1,
        beta1=0.9,
        beta2=0.999,
        epsilon=1e-08
    )

    assert a.learning_rate == 0.1
    assert a.beta1 == 0.9
    assert a.beta2 == 0.999
    assert a.epsilon == 1e-08

    assert a.get_params() == {
        "learning_rate": 0.1,
        "beta1": 0.9,
        "beta2": 0.999,
        "epsilon": 1e-08
    }