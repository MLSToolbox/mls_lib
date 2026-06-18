""" Path: Object that represents a file path. """
from pathlib import Path as SysPath
from .object import Object

class Path(Object):
    """ Path: Object that represents a file path. """
    def __init__(self, value: str = ""):
        self._value = SysPath(value) if value else SysPath()
    
    def set_path(self, value: str):
        """ Set the path value. """
        self._value = SysPath(value)

    def get_path(self) -> str:
        """ Get the path value as a string. """
        return str(self._value)

    def __str__(self) -> str:
        return self.get_path()