import json
from pathlib import Path

import onnx
import pytest

from mls_lib.deployment import OnnxSaveModel
from mls_lib.objects.path import Path as PathOutput
from mls_lib.orchestration import Metadata


class TestOnnxSaveModel:
    class _WrappedModel:
        def __init__(self, model):
            # Mimics wrappers returned by other tasks in the pipeline.
            self.model = model

    def test_execute_saves_model_in_relative_path(self, tmp_path, monkeypatch):
        """Tests that a model is saved to a relative path."""
        # Relative paths must be resolved against current working directory.
        monkeypatch.chdir(tmp_path)

        model = onnx.ModelProto()
        relative_path = "artifacts/model.onnx"
        model_version = "1.0.1"

        task = OnnxSaveModel(path=relative_path, version=model_version)
        task.set_data(model=model)
        task.execute()

        # Task should always expose the final path as PathOutput.
        saved_path_obj = task.get_output("saved_model_path")
        assert isinstance(saved_path_obj, PathOutput)
        assert saved_path_obj.get_path().endswith("artifacts/model.onnx")
        assert Path(saved_path_obj.get_path()).exists()

    def test_execute_saves_model_in_absolute_path(self, tmp_path):
        """Tests that a model is saved to an absolute path."""
        # Absolute paths should be used as-is without cwd rewriting.
        model = onnx.ModelProto()
        absolute_path = tmp_path / "out" / "model.onnx"
        model_version = "1.0.2"

        task = OnnxSaveModel(path=str(absolute_path), version=model_version)
        task.set_data(model=model)
        task.execute()

        saved_path_obj = task.get_output("saved_model_path")
        assert isinstance(saved_path_obj, PathOutput)
        assert saved_path_obj.get_path() == str(absolute_path)
        assert absolute_path.exists()

    def test_execute_creates_parent_directories(self, tmp_path):
        """Tests that parent directories are created when they do not exist."""
        # Save task must ensure parent directories exist before writing model.
        model = onnx.ModelProto()
        target_path = tmp_path / "nested" / "models" / "trained.onnx"
        model_version = "1.0.3"

        task = OnnxSaveModel(path=str(target_path), version=model_version)
        task.set_data(model=model)
        task.execute()

        assert target_path.parent.exists()
        assert target_path.exists()

    def test_execute_saves_underlying_model_when_wrapped(self, tmp_path):
        """Tests that wrapped models are unwrapped before save call."""
        # Save task should unwrap model containers transparently.
        task = OnnxSaveModel(path=str(tmp_path / "wrapped" / "model.onnx"), version="1.0.4")
        wrapped_model = self._WrappedModel(model=onnx.ModelProto())

        task.set_data(model=wrapped_model)
        task.execute()

        assert Path(task.get_output("saved_model_path").get_path()).exists()

    def test_execute_raises_value_error_when_path_is_empty(self):
        """Tests that execute raises ValueError when path is empty."""
        # Path validation should happen before writing or metadata creation.
        task = OnnxSaveModel(path="", version="1.0.5")
        task.set_data(model={"name": "demo-model", "version": 5})

        with pytest.raises(ValueError, match="requires a non-empty path"):
            task.execute()

    def test_execute_creates_metadata_file(self, tmp_path):
        """Tests that the metadata sidecar file is created with expected content."""
        # Metadata should preserve pipeline provenance in a sidecar JSON.
        Metadata.resetMetadata()
        Metadata.addDataCleaningEntry(
            Metadata.DataCleaningOperation.REPLACE_NULL_TEXT,
            columns=["city"],
            replacement_values=["unknown"],
        )

        model = onnx.ModelProto()
        target_path = tmp_path / "metadata" / "model.onnx"
        task = OnnxSaveModel(path=str(target_path), version="3.0.0")
        task.set_data(model=model)
        task.execute()

        metadata_path = tmp_path / "metadata" / "model.onnx.metadata.json"
        assert metadata_path.exists()

        metadata_content = json.loads(metadata_path.read_text(encoding="utf-8"))
        assert metadata_content["artifact_type"] == "onnx"
        assert metadata_content["version"] == "3.0.0"
        assert metadata_content["model_name"] == "ModelProto"
        assert metadata_content["data_cleaning"] == [
            {
                "type": "replace_null_text",
                "columns": ["city"],
                "replacement_values": ["unknown"],
            }
        ]
