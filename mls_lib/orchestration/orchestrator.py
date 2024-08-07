class Orchestrator:
    def __init__(self):
        """
        Initializes a new instance of the class.

        This constructor initializes the `steps` dictionary and the `step_keys` list. It also calls the constructor of the parent class.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__()
        self.steps = dict()
        self.step_keys = []
    
    def add(self, step_key, step):
        """
        Adds a step to the orchestrator.

        Args:
            step_key (str): The key to identify the step.
            step (Step): The step to be added.

        Returns:
            None
        """
        self.step_keys.append(step_key)
        self.steps[step_key] = step
    
    def getStepOutput(self, step_key, port):
        """
        Get the output of a step with the given key and port.

        Args:
            step_key (str): The key of the step.
            port (str): The port of the output.

        Returns:
            The output of the step with the given key and port.
        """
        return self.steps[step_key].getOutput(port)
    
    def clear(self):
        """
        Clear the steps in the orchestrator.

        This function clears the `steps` and `step_keys` attributes of the `Orchestrator` class by empting them.

        Parameters:
            None

        Returns:
            None
        """
        self.steps = dict()
        self.step_keys = []

    def execute(self):
        """
        Executes all the steps in the orchestrator.

        This method iterates over the `step_keys` list and calls the `execute` method of each step in the `steps` dictionary.

        Parameters:
            None

        Returns:
            None
        """
        finished = False
        i = 0
        finish_count = 0
        while (not finished):
            step_key = self.step_keys[i]
            step = self.steps[step_key]
            if (step.isReady() and (not step.isFinished())):
                # print("Executing step: " + str(type(step)))
                step.execute()
                finish_count += 1
            
            i = (i + 1) % len(self.step_keys)

            finished = (finish_count == len(self.step_keys))