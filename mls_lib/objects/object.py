""" Object: Component that holds data. """
from copy import deepcopy
class Object:
    """ Object: Component that holds data. """
    def __init__(self) -> None:
        pass
    def __str__(self) -> str:
        return "Obj"

    def __repr__(self) -> str:
        return "Obj"

    def copy(self):
        """ Returns a copy of the object. """
        return deepcopy(self)
    