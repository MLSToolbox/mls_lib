""" Pipeline Class"""
class Pipeline:
    """ Pipeline Class"""
    def __init__(self):
        super().__init__()
        self.steps = []
    def add(self, step):
        self.steps.append(step)

    def clear(self):
        self.steps = []

    def execute(self):
        for step in self.steps:
            step.execute()