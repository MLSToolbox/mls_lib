import joblib
import json
import pytest

from mls_lib.deployment import JoblibSaveModel
from mls_lib.objects.path import Path as PathOutput
from mls_lib.orchestration import Metadata


class TestJoblibSaveModel:
    class _WrappedModel:
        def __init__(self, model):
            self.model = model

    def test_execute_saves_model_in_relative_path(self, tmp_path, monkeypatch):
        """Tests that a model is saved to a relative path and can be loaded back."""
        # Prepare: isolate the current working directory for relative path resolution.
        monkeypatch.chdir(tmp_path)

        # Prepare: test data and relative output path.
        model = {"name": "demo-model", "version": 1}
        relative_path = "artifacts/model.joblib"
        model_version = "1.0.1"

        # Execute: configure task input and execute.
        task = JoblibSaveModel(path=relative_path, version=model_version)
        task.set_data(model=model)
        task.execute()

        # Assert: output path and serialized content are correct.
        saved_path_obj = task.get_output("saved_model_path")
        assert isinstance(saved_path_obj, PathOutput)
        assert saved_path_obj.get_path().endswith("artifacts/model.joblib")

        loaded_model = joblib.load(saved_path_obj.get_path())
        assert loaded_model == model

    def test_execute_saves_model_in_absolute_path(self, tmp_path):
        """Tests that a model is saved to an absolute path and can be loaded back."""
        # Prepare: test data and absolute output path.
        model = {"name": "demo-model", "version": 2}
        absolute_path = tmp_path / "out" / "model.joblib"
        model_version = "1.0.2"

        # Execute: configure task input and execute.
        task = JoblibSaveModel(path=str(absolute_path), version=model_version)
        task.set_data(model=model)

        task.execute()

        # Assert: output path and serialized content are correct.
        saved_path_obj = task.get_output("saved_model_path")
        assert isinstance(saved_path_obj, PathOutput)
        assert saved_path_obj.get_path() == str(absolute_path)
        assert absolute_path.exists()

        loaded_model = joblib.load(absolute_path)
        assert loaded_model == model

    def test_execute_creates_parent_directories(self, tmp_path):
        """Tests that parent directories are created when they do not exist."""
        # Prepare: test data and a path with missing parent directories.
        model = {"name": "demo-model", "version": 3}
        target_path = tmp_path / "nested" / "models" / "trained.joblib"
        model_version = "1.0.3"

        # Execute: configure task input and execute.
        task = JoblibSaveModel(path=str(target_path), version=model_version)
        task.set_data(model=model)

        task.execute()

        # Assert: directories and file are created.
        assert target_path.parent.exists()
        assert target_path.exists()

    def test_execute_saves_underlying_model_when_wrapped(self, tmp_path):
        """Tests that wrapped models are unwrapped before serialization."""
        # Prepare: wrap a native model-like payload inside a container object.
        task = JoblibSaveModel(path=str(tmp_path / "wrapped" / "model.joblib"), version="1.0.4")
        wrapped_model = self._WrappedModel(model={"name": "demo-model", "version": 4})

        # Execute: configure task input and execute.
        task.set_data(model=wrapped_model)
        task.execute()

        # Assert: the inner payload is what gets serialized.
        saved_path_obj = task.get_output("saved_model_path")
        loaded_model = joblib.load(saved_path_obj.get_path())
        assert loaded_model == {"name": "demo-model", "version": 4}

    def test_execute_raises_value_error_when_path_is_empty(self):
        """Tests that execute raises ValueError when path is empty."""
        # Prepare: configure a task without an output path.
        task = JoblibSaveModel(path="", version="1.0.5")
        task.set_data(model={"name": "demo-model", "version": 5})

        # Assert: path is required and missing path raises ValueError.
        with pytest.raises(ValueError, match="requires a non-empty path"):
            task.execute()

    def test_execute_creates_metadata_file(self, tmp_path):
        """Tests that the metadata sidecar file is created with expected content."""
        Metadata.resetMetadata()
        Metadata.addDataCleaningEntry(
            Metadata.DataCleaningOperation.REPLACE_NULL_ZERO,
            columns=["age"],
            replacement_values=[0],
        )

        model = {"name": "demo-model", "version": 6}
        target_path = tmp_path / "metadata" / "model.joblib"
        task = JoblibSaveModel(path=str(target_path), version="2.1.0")
        task.set_data(model=model)
        task.execute()

        metadata_path = tmp_path / "metadata" / "model.joblib.metadata.json"
        assert metadata_path.exists()

        metadata_content = json.loads(metadata_path.read_text(encoding="utf-8"))
        assert metadata_content["artifact_type"] == "joblib"
        assert metadata_content["version"] == "2.1.0"
        assert metadata_content["model_name"] == "dict"
        assert metadata_content["data_cleaning"] == [
            {
                "type": "replace_null_zero",
                "columns": ["age"],
                "replacement_values": [0],
            }
        ]