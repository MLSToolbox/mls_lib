""" ONNX SAVE MODEL"""
from pathlib import Path as SysPath
import json

import onnx

from mls_lib.objects.data_frame import DataFrame
from mls_lib.objects.models.model import Model
from mls_lib.objects import Path as PathOutput
from mls_lib.orchestration import Metadata
from mls_lib.orchestration.task import Task

class OnnxSaveModel(Task):
    """ ONNX Save Model """
    def __init__(self, model_name: str = "", version: str = "") -> None:
        super().__init__()
        self.model = Model()
        self.features = DataFrame()
        self.model_name = model_name
        self.version = version if version else "1.0.0"

    def set_data(self, model, features=None) -> None:
        """ Stores model received from stage wiring.
        Parameters:
            model: The model to be saved.
            features: Optional sample input used to infer ONNX input shape.
        Returns:
            None
        """
        self.model = model
        if features is not None:
            self.features = features

    def _unwrap_model(self, model):
        # Training tasks in this project often return wrappers with .model inside.
        # The converter needs the raw estimator instance.
        if hasattr(model, "model") and getattr(model, "model") is not None:
            return getattr(model, "model")
        return model

    def _get_n_features(self, features: DataFrame) -> int:
        feature_data = features.get_data()

        if feature_data is None:
            raise ValueError("OnnxSaveModel requires non-empty features to infer input shape")

        if len(feature_data.shape) < 2:
            raise ValueError("OnnxSaveModel expected 2D features with a valid shape")

        n_features = int(feature_data.shape[1])
        if n_features <= 0:
            raise ValueError("OnnxSaveModel inferred an invalid number of features")
        return n_features

    def _get_stable_opset(self) -> int:
        # Use a broadly supported stable opset while respecting runtime maximum.
        max_runtime_opset = int(onnx.defs.onnx_opset_version())
        return min(17, max_runtime_opset)

    def _ensure_onnx_model(self, model):
        model_to_convert = self._unwrap_model(model)
        if model_to_convert is None:
            raise ValueError("OnnxSaveModel requires a model input")

        if isinstance(model_to_convert, onnx.ModelProto):
            return model_to_convert

        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import FloatTensorType

        n_features = self._get_n_features(self.features)
        return convert_sklearn(
            model_to_convert,
            initial_types=[("input", FloatTensorType([None, n_features]))],
            target_opset=self._get_stable_opset(),
        )

    def execute(self) :
        model_name = self.model_name.strip()
        if not model_name:
            raise ValueError("OnnxSaveModel requires a non-empty model_name")

        model_to_save = self._ensure_onnx_model(self.model)

        # Always write artifacts in ./artifacts using model_name as filename.
        normalized_name = SysPath(model_name).name
        if normalized_name.endswith(".onnx"):
            normalized_name = normalized_name[:-5]

        artifacts_dir = SysPath.cwd() / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        target_path = artifacts_dir / f"{normalized_name}.onnx"

        
        onnx.save(model_to_save, str(target_path))

        metadata_content = Metadata.getMetadata()
        metadata_content["model_name"] = self.model_name
        metadata_content["version"] = self.version
        metadata_content["artifact_type"] = "onnx"

        metadata_path = SysPath(f"{target_path}.metadata.json")

        # Use text mode with UTF-8 so the metadata file stays human-readable
        # and compatible across environments.
        with open(metadata_path, "w", encoding="utf-8") as metadata_file:
            # Write pretty JSON (indent=2) to make diffs and manual inspection easy.
            json.dump(metadata_content, metadata_file, ensure_ascii=False, indent=2)

        self._set_output("saved_model_path", PathOutput(str(target_path)))