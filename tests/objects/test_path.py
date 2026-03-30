from pathlib import Path as SysPath

from mls_lib.objects.path import Path
from pytest import fixture


@fixture
def path_object():
    return Path()


def test_empty_path(path_object: Path):
    """ Tests that the default path is empty. """
    assert path_object.get_path() == str(SysPath())
    assert str(path_object) == str(SysPath())


def test_set_and_get_path(path_object: Path):
    """ Tests that the path can be set and retrieved correctly. """
    path_object.set_path("models/model.joblib")
    assert path_object.get_path() == str(SysPath("models/model.joblib"))
    assert str(path_object) == str(SysPath("models/model.joblib"))


def test_init_with_path():
    """ Tests that the path can be initialized with a value. """
    path_object = Path("artifacts/final.joblib")
    assert path_object.get_path() == str(SysPath("artifacts/final.joblib"))


def test_copy_path(path_object: Path):
    """ Tests that the path can be copied correctly. """
    path_object.set_path("a/b/c.txt")
    path_copy = path_object.copy()

    assert path_copy is not path_object
    assert isinstance(path_copy, Path)
    assert path_copy.get_path() == path_object.get_path()