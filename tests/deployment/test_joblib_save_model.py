import joblib
import pytest

from mls_lib.deployment import JoblibSaveModel
from mls_lib.objects.path import Path as PathOutput


class TestJoblibSaveModel:
    class _WrappedModel:
        def __init__(self, model):
            self.model = model

    def test_execute_saves_model_in_artifacts_folder(self, tmp_path, monkeypatch):
        """Tests that a model is saved under ./artifacts with .joblib extension."""
        monkeypatch.chdir(tmp_path)

        # Prepare: test data and model name.
        model = {"name": "demo-model", "version": 1}
        model_name = "model"
        model_version = "1.0.1"

        # Execute: configure task input and execute.
        task = JoblibSaveModel(model_name=model_name, version=model_version)
        task.set_data(model=model)
        task.execute()

        # Assert: output path and serialized content are correct.
        saved_path_obj = task.get_output("saved_model_path")
        assert isinstance(saved_path_obj, PathOutput)
        assert saved_path_obj.get_path() == str(tmp_path / "artifacts" / "model.joblib")

        loaded_model = joblib.load(saved_path_obj.get_path())
        assert loaded_model == model

    def test_execute_creates_artifacts_directory(self, tmp_path, monkeypatch):
        """Tests that artifacts directory is created automatically."""
        monkeypatch.chdir(tmp_path)

        task = JoblibSaveModel(model_name="trained", version="1.0.2")
        task.set_data(model={"name": "demo-model", "version": 2})
        task.execute()

        assert (tmp_path / "artifacts").exists()
        assert (tmp_path / "artifacts" / "trained.joblib").exists()

    def test_execute_saves_underlying_model_when_wrapped(self, tmp_path, monkeypatch):
        """Tests that wrapped models are unwrapped before serialization."""
        monkeypatch.chdir(tmp_path)

        # Prepare: wrap a native model-like payload inside a container object.
        task = JoblibSaveModel(model_name="wrapped_model", version="1.0.4")
        wrapped_model = self._WrappedModel(model={"name": "demo-model", "version": 4})

        # Execute: configure task input and execute.
        task.set_data(model=wrapped_model)
        task.execute()

        # Assert: the inner payload is what gets serialized.
        saved_path_obj = task.get_output("saved_model_path")
        loaded_model = joblib.load(saved_path_obj.get_path())
        assert loaded_model == {"name": "demo-model", "version": 4}

    def test_execute_raises_value_error_when_model_name_is_empty(self):
        """Tests that execute raises ValueError when model_name is empty."""
        # Prepare: configure a task without a model name.
        task = JoblibSaveModel(model_name="", version="1.0.5")
        task.set_data(model={"name": "demo-model", "version": 5})

        # Assert: model_name is required and missing name raises ValueError.
        with pytest.raises(ValueError, match="requires a non-empty model_name"):
            task.execute()
