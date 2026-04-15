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

    def test_execute_saves_model_in_artifacts_folder(self, tmp_path, monkeypatch):
        """Tests that a model is saved under ./artifacts with .onnx extension."""
        monkeypatch.chdir(tmp_path)

        model = onnx.ModelProto()
        model_name = "model"
        model_version = "1.0.1"

        task = OnnxSaveModel(model_name=model_name, version=model_version)
        task.set_data(model=model)
        task.execute()

        # Task should always expose the final path as PathOutput.
        saved_path_obj = task.get_output("saved_model_path")
        assert isinstance(saved_path_obj, PathOutput)
        assert saved_path_obj.get_path() == str(tmp_path / "artifacts" / "model.onnx")
        assert Path(saved_path_obj.get_path()).exists()

    def test_execute_creates_artifacts_directory(self, tmp_path, monkeypatch):
        """Tests that artifacts directory is created automatically."""
        monkeypatch.chdir(tmp_path)

        task = OnnxSaveModel(model_name="trained", version="1.0.2")
        task.set_data(model=onnx.ModelProto())
        task.execute()

        assert (tmp_path / "artifacts").exists()
        assert (tmp_path / "artifacts" / "trained.onnx").exists()

    def test_execute_saves_underlying_model_when_wrapped(self, tmp_path, monkeypatch):
        """Tests that wrapped models are unwrapped before save call."""
        monkeypatch.chdir(tmp_path)

        # Save task should unwrap model containers transparently.
        task = OnnxSaveModel(model_name="wrapped_model", version="1.0.4")
        wrapped_model = self._WrappedModel(model=onnx.ModelProto())

        task.set_data(model=wrapped_model)
        task.execute()

        assert Path(task.get_output("saved_model_path").get_path()).exists()

    def test_execute_raises_value_error_when_model_name_is_empty(self):
        """Tests that execute raises ValueError when model_name is empty."""
        # model_name validation should happen before writing or metadata creation.
        task = OnnxSaveModel(model_name="", version="1.0.5")
        task.set_data(model={"name": "demo-model", "version": 5})

        with pytest.raises(ValueError, match="requires a non-empty model_name"):
            task.execute()

    def test_execute_creates_metadata_file(self, tmp_path, monkeypatch):
        """Tests that the metadata sidecar file is created with expected content."""
        monkeypatch.chdir(tmp_path)

        # Metadata should preserve pipeline provenance in a sidecar JSON.
        Metadata.resetMetadata()
        Metadata.addDataCleaningEntry(
            Metadata.DataCleaningOperation.REPLACE_NULL_TEXT,
            columns=["city"],
            replacement_values=["unknown"],
        )

        model = onnx.ModelProto()
        task = OnnxSaveModel(model_name="model", version="3.0.0")
        task.set_data(model=model)
        task.execute()

        metadata_path = tmp_path / "artifacts" / "model.onnx.metadata.json"
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
