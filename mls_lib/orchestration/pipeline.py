""" Pipeline Class"""
class Pipeline:
    """Pipeline: Component that orchestrates a sequence of steps in a pipeline. """
    def __init__(self):
        """Initializes a new instance of the Pipeline class.

        This constructor initializes a new instance of the Pipeline class
        and sets the `steps` field to an empty list.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__()
        self.steps = []
    def add(self, step):
        """Adds a step to the pipeline.

        This function adds a step to the `steps` list 
        of the `Pipeline` class.

        Parameters:
            step (Step): The step to add to the pipeline.

        Returns:
            None
        """
        self.steps.append(step)

    def clear(self):
        """Clear the  in the pipeline.

        This function clears the `steps` attribute of 
        the `Pipeline` class by empting it.

        Parameters:
            None

        Returns:
            None
        """
        self.steps = []

    def execute(self):
        """Execute all the steps in the pipeline.

        This method iterates over the `steps` list and calls the
        `execute` method of each step in the `steps` list.

        Parameters:
            None

        Returns:
            None
        """
        for step in self.steps:
            step.execute()