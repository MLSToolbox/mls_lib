""" Model artifact loader. """

from pathlib import Path
import json
import shutil

from mls_lib.objects import Path as PathOutput
from mls_lib.orchestration import Metadata
from mls_lib.orchestration.task import Task


class ModelLoader(Task):
    """Moves a model artifact to artifacts and exposes its path."""

    def __init__(self, model_filename: str = "", preprocessing_steps=None) -> None:
        super().__init__()
        self.model_filename = model_filename
        self.preprocessing_steps = preprocessing_steps or []

    def execute(self) -> None:
        filename = self.model_filename.strip()
        if not filename:
            raise ValueError("ModelLoader requires a non-empty model_filename")

        source_model_path = Path.cwd() / filename
        if not source_model_path.exists() or not source_model_path.is_file():
            raise FileNotFoundError(f"ModelLoader could not find model file: {source_model_path}")

        artifacts_dir = Path.cwd() / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        target_model_path = artifacts_dir / source_model_path.name
        if source_model_path.resolve() != target_model_path.resolve():
            if target_model_path.exists():
                target_model_path.unlink()
            shutil.move(str(source_model_path), str(target_model_path))

        extension = target_model_path.suffix.lower()
        if extension not in {".joblib", ".onnx"}:
            raise ValueError("ModelLoader supports only .joblib or .onnx files")

        metadata_content = Metadata.getMetadata()
        metadata_content["data_cleaning"] = self._normalize_preprocessing_steps(self.preprocessing_steps)
        metadata_content["model_name"] = target_model_path.name
        metadata_content["version"] = metadata_content.get("version", "1.0.0")
        metadata_content["artifact_type"] = extension.lstrip(".")

        metadata_path = Path(f"{target_model_path}.metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as metadata_file:
            json.dump(metadata_content, metadata_file, ensure_ascii=False, indent=2)

        self._set_output("model_path", PathOutput(str(target_model_path)))

    def _normalize_preprocessing_steps(self, preprocessing_steps) -> list[dict]:
        """Normalizes cleaning_map entries into metadata format."""
        if not preprocessing_steps:
            return []

        normalized_entries = []
        for step in preprocessing_steps:
            if not isinstance(step, dict):
                continue

            cleaning_type = step.get("cleaning_type", "")
            column = step.get("column", "")
            replacement_value = step.get("replacement_value", "")

            columns = [str(column)] if str(column).strip() else []
            replacement_values = []
            if isinstance(replacement_value, list):
                replacement_values = replacement_value
            elif str(replacement_value).strip():
                replacement_values = [replacement_value]

            normalized_entries.append(
                {
                    "type": str(cleaning_type).strip().lower().replace(" ", "_"),
                    "columns": columns,
                    "replacement_values": replacement_values,
                }
            )

        return normalized_entries
