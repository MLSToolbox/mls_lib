"""Deploys a pre-serialized model artifact into a Docker container."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path as SysPath

from mls_lib.orchestration.task import Task


class DeployWithDocker(Task):
    """Builds a Docker image with a prepared model artifact path."""

    def __init__(self, image_name: str, port) -> None:
        super().__init__()
        self.image_name = image_name.strip() if image_name else "mls-model-service"
        self.port = self._resolve_port(port)

        self.model_path_input: str = ""

    def set_data(self, model_path) -> None:
        """Receives the model path from stage wiring and normalizes it."""
        if model_path is None:
            raise ValueError("DeployWithDocker requires model_path input")

        raw_path = model_path.get_path()
        if not raw_path:
            raise ValueError("DeployWithDocker requires model_path input")

        self.model_path_input = self._resolve_model_path(raw_path)

    def _resolve_model_path(self, raw_path: str) -> str:
        """Resolves the input model path relative to the current workspace."""
        candidate = SysPath(str(raw_path).strip())
        if not candidate.is_absolute():
            candidate = SysPath.cwd() / candidate
        return str(candidate)

    def execute(self):
        source_model_path = SysPath(self.model_path_input)
        if not source_model_path.exists() or not source_model_path.is_file():
            raise FileNotFoundError(
                f"DeployWithDocker could not find model artifact: {source_model_path}"
            )

        deployment_dir = self._prepare_deployment_directory()

        self._write_runtime_assets(
            deployment_dir=deployment_dir,
            model_filename=source_model_path.name,
        )

        self._build_image(deployment_dir, source_model_path.name)

        deployment_info = {
            "image_name": self.image_name,
            "port": self.port,
            "deployment_dir": str(deployment_dir),
            "model_path": str(source_model_path),
            "image_built": True,
        }
        self._set_output("deployment_info", deployment_info)

    def _resolve_port(self, port) -> int:
        """Resolves and validates host port, defaulting to 8000."""
        if port in (None, ""):
            return 8000

        resolved = int(port)
        if resolved <= 0:
            raise ValueError("DeployWithDocker requires a positive port")
        return resolved

    def _prepare_deployment_directory(self) -> SysPath:
        """Ensures artifacts/deployment exists and returns its path."""
        deployment_dir = SysPath.cwd() / "artifacts" / "deployment"
        deployment_dir.mkdir(parents=True, exist_ok=True)
        return deployment_dir

    def _write_runtime_assets(self, deployment_dir: SysPath, model_filename: str) -> None:
        """Creates runtime files needed by Docker image to serve inference later."""
        config_path = deployment_dir / "deployment_config.json"
        requirements_path = deployment_dir / "requirements.txt"
        dockerfile_path = deployment_dir / "Dockerfile"

        config_content = {
            "model_filename": model_filename,
            "model_extension": SysPath(model_filename).suffix.lower(),
            "model_artifact_path": f"artifacts/{model_filename}",
        }
        self._write_json_file(config_path, config_content)

        requirements_content = self._load_deployment_template("requirements.txt.template")
        dockerfile_content = self._load_deployment_template("Dockerfile.template")

        requirements_path.write_text(requirements_content, encoding="utf-8")
        dockerfile_path.write_text(dockerfile_content, encoding="utf-8")

    def _load_deployment_template(self, template_name: str) -> str:
        """Loads a deployment template from package templates directory."""
        template_path = SysPath(__file__).resolve().parent / "templates" / template_name
        if not template_path.exists() or not template_path.is_file():
            raise FileNotFoundError(f"DeployWithDocker could not find template: {template_path}")
        return template_path.read_text(encoding="utf-8")

    def _build_image(self, deployment_dir: SysPath, model_filename: str) -> None:
        """Builds Docker image that packages model artifact and metadata."""
        self._run_command(
            [
                "docker",
                "build",
                "-f",
                str(deployment_dir / "Dockerfile"),
                "--build-arg",
                f"MODEL_FILENAME={model_filename}",
                "-t",
                self.image_name,
                ".",
            ],
            cwd=SysPath.cwd(),
            check=True,
        )

    def _run_command(self, cmd: list[str], cwd: SysPath, check: bool) -> None:
        """Executes system command and reports stderr on failure."""
        subprocess.run(
            cmd,
            cwd=str(cwd),
            check=check,
            capture_output=True,
            text=True,
        )

    def _write_json_file(self, target_path: SysPath, content: dict) -> None:
        """Writes JSON files using UTF-8 and pretty indentation for readability."""
        with open(target_path, "w", encoding="utf-8") as file_obj:
            json.dump(content, file_obj, ensure_ascii=False, indent=2)
