"""class Stage: Represents a stage in the pipeline. """
import uuid
from mls_lib.orchestration.step import Step

class Stage(Step):
    """ Represents a stage in the pipeline. """

    def __init__(self):
        """ Initializes a new instance of the class. """
        super().__init__()
        self.steps = {}

    def add_step(self, step, **inputs):
        """ Adds a step to the stage. """
        step_key = str(uuid.uuid4())
        self.steps[step_key] = (step, inputs)
    
    def add_output(self, port, step_port):
        """ Adds an output to the stage. """
        self.outputs[port] = step_port

    def get_output(self, port):
        """ Get the output of the stage. """
        output_step, output_port = self.outputs[port]
        return output_step.get_output(output_port)

    def execute(self):
        """ Executes all the steps in the stage. """
        step_keys = list(self.steps.keys())
        finish_count = 0
        while finish_count < len(self.steps):
            for step_key in step_keys:
                if not self.__is_step_ready(step_key):
                    continue
                step, inputs = self.steps[step_key]
                data = {}
                for port, step_port in inputs.items():
                    input_step, input_port = step_port
                    data[port] = input_step.get_output(input_port)
                if len(data) > 0:
                    step.set_data(**data)
                step.execute()
                step.finish_execution()
                finish_count += 1
        self.finish_execution()
    
    def __is_step_ready(self, step_key):
        """ Checks if the step is ready. """
        step, inputs = self.steps[step_key]
        if step.is_finished():
            return False
        for _, input_step_port in inputs.items():
            input_step, _ = input_step_port
            if not input_step.is_finished():
                return False
        return True