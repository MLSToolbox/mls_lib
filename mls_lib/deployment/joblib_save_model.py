""" JOBLIB SAVE MODEL """
from mls_lib.orchestration.task import Task
import joblib

class JoblibSaveModel(Task):
    """ Joblib Save Model """
    def __init__(self) -> None:
        super().__init__()

    def execute(self) :
        model = self.get_input("model")
        path = self.get_parameter("path")
        joblib.dump(model, path)