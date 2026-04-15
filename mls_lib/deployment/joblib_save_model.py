""" JOBLIB SAVE MODEL """
from mls_lib.objects.models.model import Model
from mls_lib.orchestration.task import Task
from mls_lib.objects import Path as PathOutput
from mls_lib.orchestration import Metadata

from pathlib import Path as SysPath
import json
import joblib

class JoblibSaveModel(Task):
    """ Joblib Save Model """
    def __init__(self, model_name: str = "", version: str = "") -> None:
        super().__init__()
        self.model = Model()
        self.model_name = model_name
        self.version = version if version else "1.0.0"

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

        model_name = self.model_name.strip()
        if not model_name:
            raise ValueError("JoblibSaveModel requires a non-empty model_name")

        # Always write artifacts in ./artifacts using model_name as filename.
        normalized_name = SysPath(model_name).name
        if normalized_name.endswith(".joblib"):
            normalized_name = normalized_name[:-7]

        artifacts_dir = SysPath.cwd() / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        target_path = artifacts_dir / f"{normalized_name}.joblib"

        joblib.dump(model_to_save, target_path)

        metadata_content = Metadata.getMetadata()
        metadata_content["model_name"] = self.model_name
        metadata_content["version"] = self.version
        metadata_content["artifact_type"] = "joblib"

        metadata_path = SysPath(f"{target_path}.metadata.json")

        # Use text mode with UTF-8 so the metadata file stays human-readable
        # and compatible across environments.
        with open(metadata_path, "w", encoding="utf-8") as metadata_file:
            # Write pretty JSON (indent=2) to make diffs and manual inspection easy.
            json.dump(metadata_content, metadata_file, ensure_ascii=False, indent=2)

        self._set_output("saved_model_path", PathOutput(str(target_path)))