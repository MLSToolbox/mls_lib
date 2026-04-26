from pathlib import Path

import joblib
import onnx
import pytest

from mls_lib.data_collection import ModelLoader


class TestModelLoader:
    def test_loads_joblib_model_from_project_root(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        model_path = tmp_path / "model.joblib"
        expected = {"name": "demo", "version": 1}
        joblib.dump(expected, model_path)

        task = ModelLoader(model_filename="model.joblib")
        task.execute()

        assert task.get_output("model") == expected

    def test_loads_onnx_model_from_project_root(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        model_path = tmp_path / "model.onnx"
        expected = onnx.ModelProto()
        onnx.save(expected, str(model_path))

        task = ModelLoader(model_filename="model.onnx")
        task.execute()

        loaded = task.get_output("model")
        assert isinstance(loaded, onnx.ModelProto)

    def test_raises_when_filename_empty(self):
        task = ModelLoader(model_filename="")

        with pytest.raises(ValueError, match="non-empty model_filename"):
            task.execute()

    def test_raises_when_file_not_found(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        task = ModelLoader(model_filename="missing.joblib")

        with pytest.raises(FileNotFoundError, match="could not find model file"):
            task.execute()

    def test_raises_for_unsupported_extension(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        unsupported = tmp_path / "model.pkl"
        unsupported.write_text("not supported", encoding="utf-8")

        task = ModelLoader(model_filename="model.pkl")

        with pytest.raises(ValueError, match="supports only .joblib or .onnx"):
            task.execute()
