""" Pipeline Class"""
class Pipeline:
    """Pipeline: Component that orchestrates a sequence of steps in a pipeline. """
    def __init__(self):
        """Initializes a new instance of the Pipeline class.

        This constructor initializes a new instance of the Pipeline class
        and sets the `tasks` field to an empty list.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__()
        self.tasks = []
    def add(self, task):
        """Adds a task to the pipeline.

        This function adds a task to the `tasks` list 
        of the `Pipeline` class.

        Parameters:
            task (Task): The task to add to the pipeline.

        Returns:
            None
        """
        self.tasks.append(task)

    def clear(self):
        """Clear the tasks in the pipeline.

        This function clears the `tasks` attribute of 
        the `Pipeline` class by empting it.

        Parameters:
            None

        Returns:
            None
        """
        self.tasks = []

    def execute(self):
        """Execute all the tasks in the pipeline.

        This method iterates over the `tasks` list and calls the
        `execute` method of each task in the `tasks` list.

        Parameters:
            None

        Returns:
            None
        """
        for task in self.tasks:
            task.execute()