""" Pipeline Class"""
class Pipeline:
    """ Pipeline Class"""
    def __init__(self):
        """
        Initializes a new instance of the class.

        This constructor initializes the `steps` dictionary and the `step_keys` list.
        It also calls the constructor of the parent class.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__()
        self.steps = []
    def add(self, step):
        self.steps.append(step)

    def clear(self):
        self.steps = {}

    def execute(self):
        finished = len(self.steps) == 0
        i = 0
        finish_count = 0
        while not finished:
            step = self.steps[i]
            if (step.is_ready() and (not step.is_finished())):
                # print("Executing step: " + str(type(step)))
                step.execute()
                step.finish_execution()
                finish_count += 1
            i = (i + 1) % len(self.steps)

            finished = finish_count == len(self.steps)
