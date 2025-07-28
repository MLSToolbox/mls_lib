from pytest import fixture
from ...mls_lib.orchestration import Pipeline

@fixture
def pipeline():
    return Pipeline()

def test_empty_pipeline(pipeline):
    assert pipeline
    assert pipeline.stages == {}
