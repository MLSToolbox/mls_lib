""" ONNX SAVE MODEL"""
from mls_lib.objects.models.model import Model
from mls_lib.orchestration.task import Task
from mls_lib.objects import Path as PathOutput

from pathlib import Path as SysPath
import onnx

class OnnxSaveModel(Task):
    """ ONNX Save Model """
    def __init__(self, path: str = "") -> None:
        super().__init__()
        self.model = Model()
        self.path = path

    def set_data(self, model) -> None:
        """ Stores model received from stage wiring.
        Parameters:
            model: The model to be saved.
        Returns:
            None
        """
        self.model = model

    def execute(self) :
        model = self.model
        
        # As the model is wrapped by the mls_lib, we check if it has a model attribute and save that instead.
        # Firstly, we save this wrapped model in the variable. If the model has a model attribute, we will save that instead.
        
        model_to_save = model
        if hasattr(model, "model") and getattr(model, "model") is not None:
            model_to_save = getattr(model, "model")

        path = self.path
        if not path:
            raise ValueError("OnnxSaveModel requires a non-empty path")

        # Creates the absolute path of the provided path.
        # An absolute path is the one that starts from the root directory.
        # A relative one is the one that starts from the current working directory.
        # We want the path to be absolute, to save the model in the correct location. 

        base_dir = SysPath.cwd()
        target_path = SysPath(path)

        if not target_path.is_absolute():
            target_path = base_dir / target_path
        
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        onnx.save(model_to_save, str(target_path))
        
        self._set_output("saved_model_path", PathOutput(str(target_path)))