from copy import deepcopy
class Object:
    def __init__(self) -> None:
        pass

    def copy(self):
        return deepcopy(self)