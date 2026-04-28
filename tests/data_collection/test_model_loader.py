from pathlib import Path
import json

import joblib
import onnx
import pytest

from mls_lib.data_collection import ModelLoader
from mls_lib.objects.path import Path as PathOutput


class TestModelLoader:
    def test_loads_joblib_model_from_project_root(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        model_path = tmp_path / "model.joblib"
        expected = {"name": "demo", "version": 1}
        joblib.dump(expected, model_path)

        task = ModelLoader(model_filename="model.joblib")
        task.execute()

        output = task.get_output("model_path")
        assert isinstance(output, PathOutput)
        assert output.get_path() == str(tmp_path / "artifacts" / "model.joblib")
        assert (tmp_path / "artifacts" / "model.joblib").exists()
        assert not model_path.exists()
        assert (tmp_path / "artifacts" / "model.joblib.metadata.json").exists()

    def test_loads_onnx_model_from_project_root(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        model_path = tmp_path / "model.onnx"
        expected = onnx.ModelProto()
        onnx.save(expected, str(model_path))

        task = ModelLoader(model_filename="model.onnx")
        task.execute()

        output = task.get_output("model_path")
        assert isinstance(output, PathOutput)
        assert output.get_path() == str(tmp_path / "artifacts" / "model.onnx")
        assert (tmp_path / "artifacts" / "model.onnx").exists()
        assert not model_path.exists()

    def test_builds_metadata_from_preprocessing_steps(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        expected = {"name": "demo", "version": 1}
        joblib.dump(expected, tmp_path / "model.joblib")

        task = ModelLoader(
            model_filename="model.joblib",
            preprocessing_steps=[
                {
                    "cleaning_type": "Replace Nulls Zero",
                    "column": "age",
                    "replacement_value": 0,
                }
            ],
        )
        task.execute()

        metadata_path = tmp_path / "artifacts" / "model.joblib.metadata.json"
        metadata_content = json.loads(metadata_path.read_text(encoding="utf-8"))
        assert metadata_content["artifact_type"] == "joblib"
        assert metadata_content["model_name"] == "model.joblib"
        assert metadata_content["data_cleaning"] == [
            {
                "type": "replace_nulls_zero",
                "columns": ["age"],
                "replacement_values": [0],
            }
        ]

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
