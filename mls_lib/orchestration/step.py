""" Step """

from mls_lib.objects.object import Object

class Step:
    """
    Abstract Step
    """
    def __init__(self, **inputs) -> None:
        self.inputs = inputs
        self.outputs = {}
        self.finished = False
        self.step_category = "abstract_step"

    def execute(self):
        """ Execute the step. """    
    def get_output(self, port):
        """ Get the output of the step. """
        return self.outputs[port]
    def _get_input_step(self, port):
        """ Get the step that is connected to the input port. """
        return self.inputs[port]
    def is_ready(self):
        """ Check if the step is ready. """
        for _, step in self.inputs.items():
            if not step[0].is_finished():
                return False
        return True

    def is_finished(self):
        """ Check if the step is finished. """
        return self.finished
    def _get_input(self, port) -> Object:
        """ Get the output of the step connected to this input port. """
        origin, origin_port = self.inputs[port]
        return origin.get_output(origin_port)

    def _set_output(self, port, value):
        """ Set the output of the step. """
        self.outputs[port] = value
    def _finish_execution(self):
        """ Finish the execution of the step. """
        self.finished = True
