"""class Stage: Represents a stage in the pipeline. """
import uuid
from mls_lib.orchestration.task import Step

class Stage(Step):
    """ Represents a stage in the pipeline. """
    def __init__(self, name : str):
        """ Initializes a new instance of the class. """
        super().__init__()
        self.name = name
        self.tasks = {}
        self.inputs = {}
    def __repr__(self):
        """ Returns a string representation of the stage. """
        return self.name
    def add_task(self, task, **inputs):
        """ Adds a task to the stage. """
        task_key = str(uuid.uuid4())
        self.tasks[task_key] = (task, inputs)
    def add_output(self, port, task_port):
        """ Adds an output to the stage. """
        self.outputs[port] = task_port
    def get_output(self, port):
        """ Get false output (output of the previous stages) for the tasks in the stage. """
        return self.inputs[port]  
    def get_stage_output(self, port):
        """ Get the output of the stage. """
        output_task, output_port = self.outputs[port]
        return output_task.get_output(output_port)
    def set_data(self, **kwargs):
        """ Sets the data of the stage. """
        for port, value in kwargs.items():
            self.inputs[port] = value
    def execute(self):
        """ Executes all the tasks in the stage. """
        print("Executing Stage: " + self.name)
        task_keys = list(self.tasks.keys())
        finish_count = 0
        while finish_count < len(self.tasks):
            for task_key in task_keys:
                if not self.__is_task_ready(task_key):
                    continue
                task, inputs = self.tasks[task_key]
                data = {}
                for port, task_port in inputs.items():
                    input_task, input_port = task_port
                    data[port] = input_task.get_output(input_port)
                if len(data) > 0:
                    task.set_data(**data)
                task.execute()
                task.finish_execution()
                finish_count += 1
        self.finish_execution()
    def __is_task_ready(self, task_key):
        """ Checks if the task is ready. """
        task, inputs = self.tasks[task_key]
        if task.is_finished():
            return False
        for _, input_task_port in inputs.items():
            input_task, _ = input_task_port
            if input_task is self:
                continue
            if not input_task.is_finished():
                return False
        return True
    