""" JOBLIB SAVE MODEL """
from mls_lib.orchestration.task import Task
from mls_lib.objects import Path as PathOutput
from pathlib import Path as SysPath
import joblib

class JoblibSaveModel(Task):
    """ Joblib Save Model """
    def __init__(self) -> None:
        super().__init__()

    def execute(self) :
        model = self.get_input("model")

        path = self.get_parameter("path")
        base_dir = SysPath.cwd()
        target_path = SysPath(path)

        if not target_path.is_absolute():
            target_path = base_dir / target_path
        
        target_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, target_path)
        self._set_output("saved_model_path", PathOutput(str(target_path)))