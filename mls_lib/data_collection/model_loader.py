""" Model artifact loader. """

from pathlib import Path

import joblib
import onnx

from mls_lib.orchestration.task import Task


class ModelLoader(Task):
    """Loads a model artifact from the project root (joblib or onnx)."""

    def __init__(self, model_filename: str = "") -> None:
        super().__init__()
        self.model_filename = model_filename

    def execute(self) -> None:
        filename = self.model_filename.strip()
        if not filename:
            raise ValueError("ModelLoader requires a non-empty model_filename")

        model_path = Path.cwd() / filename
        if not model_path.exists() or not model_path.is_file():
            raise FileNotFoundError(f"ModelLoader could not find model file: {model_path}")

        extension = model_path.suffix.lower()
        if extension == ".joblib":
            loaded_model = joblib.load(model_path)
        elif extension == ".onnx":
            loaded_model = onnx.load(str(model_path))
        else:
            raise ValueError("ModelLoader supports only .joblib or .onnx files")

        self._set_output("model", loaded_model)
