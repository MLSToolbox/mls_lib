from .object import Object

class DataFrame(Object):
    def __init__(self):
        self.data = None
    
    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data
