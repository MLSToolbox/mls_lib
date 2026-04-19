""" Task : Represents a task in the pipeline. """

from . step import Step

class Task(Step):
    """ Task : Represents a task in the pipeline. """

    def write_metadata(self) -> None:
        """Writes task metadata. Default implementation is no-op."""
