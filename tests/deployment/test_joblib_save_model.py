import joblib

from mls_lib.deployment import JoblibSaveModel
from mls_lib.objects.path import Path as PathOutput


class TestJoblibSaveModel:
    class _WrappedModel:
        def __init__(self, model):
            self.model = model

    def test_execute_saves_model_in_relative_path(self, tmp_path, monkeypatch):
        """ Tests that a mock model is saved in correct relative path and can be loaded back. """
        monkeypatch.chdir(tmp_path)

        task = JoblibSaveModel()
        model = {"name": "demo-model", "version": 1}
        relative_path = "artifacts/model.joblib"

        task.get_input = lambda port: model
        task.get_parameter = lambda name: relative_path

        task.execute()

        saved_path_obj = task.get_output("saved_model_path")
        assert isinstance(saved_path_obj, PathOutput)
        assert saved_path_obj.get_path().endswith("artifacts/model.joblib")

        loaded_model = joblib.load(saved_path_obj.get_path())
        assert loaded_model == model

    def test_execute_saves_model_in_absolute_path(self, tmp_path):
        """ Tests that a mock model is saved in correct absolute path and can be loaded back. """
        task = JoblibSaveModel()
        model = [1, 2, 3]
        absolute_path = tmp_path / "out" / "model.joblib"

        task.get_input = lambda port: model
        task.get_parameter = lambda name: str(absolute_path)

        task.execute()

        saved_path_obj = task.get_output("saved_model_path")
        assert isinstance(saved_path_obj, PathOutput)
        assert saved_path_obj.get_path() == str(absolute_path)
        assert absolute_path.exists()

        loaded_model = joblib.load(absolute_path)
        assert loaded_model == model

    def test_execute_creates_parent_directories(self, tmp_path):
        """ Tests that the parent directories are created if they don't exist. """
        task = JoblibSaveModel()
        model = {"ok": True}
        target_path = tmp_path / "nested" / "models" / "trained.joblib"

        task.get_input = lambda port: model
        task.get_parameter = lambda name: str(target_path)

        task.execute()

        assert target_path.parent.exists()
        assert target_path.exists()

    def test_execute_works_with_stage_set_data(self, tmp_path):
        """ Tests that stage-style set_data wiring works for model input. """
        task = JoblibSaveModel(path=str(tmp_path / "stage" / "model.joblib"))
        model = {"from_stage": True}

        task.set_data(model=model)
        task.execute()

        saved_path_obj = task.get_output("saved_model_path")
        loaded_model = joblib.load(saved_path_obj.get_path())
        assert loaded_model == model

    def test_execute_saves_underlying_model_when_wrapped(self, tmp_path):
        """ Tests that wrapped MLS models are unwrapped before being serialized. """
        task = JoblibSaveModel(path=str(tmp_path / "wrapped" / "model.joblib"))
        wrapped_model = self._WrappedModel(model={"native": "sklearn-like"})

        task.set_data(model=wrapped_model)
        task.execute()

        saved_path_obj = task.get_output("saved_model_path")
        loaded_model = joblib.load(saved_path_obj.get_path())
        assert loaded_model == {"native": "sklearn-like"}