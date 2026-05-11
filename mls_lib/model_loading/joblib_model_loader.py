""" Joblib model loader. """

from pathlib import Path
import shutil

from mls_lib.objects import Path as PathOutput
from mls_lib.orchestration.task import Task


class JoblibModelLoader(Task):
    """Moves a Joblib model artifact to artifacts and exposes its path."""

    def __init__(self, model_filename: str = "") -> None:
        super().__init__()
        self.model_filename = model_filename

    def execute(self) -> None:
        filename = self.model_filename.strip()
        if not filename:
            raise ValueError("JoblibModelLoader requires a non-empty model_filename")

        source_model_path = Path.cwd() / filename
        if not source_model_path.exists() or not source_model_path.is_file():
            raise FileNotFoundError(
                f"JoblibModelLoader could not find model file: {source_model_path}"
            )

        if source_model_path.suffix.lower() != ".joblib":
            raise ValueError("JoblibModelLoader supports only .joblib files")

        artifacts_dir = Path.cwd() / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        target_model_path = artifacts_dir / source_model_path.name
        if source_model_path.resolve() != target_model_path.resolve():
            if target_model_path.exists():
                target_model_path.unlink()
            shutil.move(str(source_model_path), str(target_model_path))

        self._set_output("model_path", PathOutput(str(target_model_path)))
