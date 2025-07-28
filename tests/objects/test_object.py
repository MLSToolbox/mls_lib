from mls_lib.objects.object import Object
from pytest import fixture

@fixture
def object():
    return Object()

def test_object(object):
    assert str(object) == "Obj"
    assert repr(object) == "Obj"
    assert object.copy() != object