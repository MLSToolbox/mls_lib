""" Step """

class Step:
    """
    Abstract Step
    """
    def __init__(self) -> None:
        self.outputs = {}
        self.finished = False
    def execute(self):
        """ Execute the step. """
    def get_output(self, port):
        """ Get the output of the step. """
        return self.outputs[port]
    def is_finished(self):
        """ Check if the step is finished. """
        return self.finished
    def _set_output(self, port, value):
        """ Set the output of the step. """
        self.outputs[port] = value
    def finish_execution(self):
        """ Finish the execution of the step. """
        self.finished = True
