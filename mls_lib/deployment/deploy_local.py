"""Deploys a pre-serialized model artifact locally without Docker."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path as SysPath

from mls_lib.orchestration.task import Task


class DeployLocal(Task):
    """Prepares local runtime assets and starts the model service."""

    def __init__(self, port) -> None:
        super().__init__()
        self.port = self._resolve_port(port)
        self.model_path_input: str = ""

    def set_data(self, model_path) -> None:
        """Receives the model path from stage wiring and normalizes it."""
        if model_path is None:
            raise ValueError("DeployLocal requires model_path input")

        raw_path = model_path.get_path()
        if not raw_path:
            raise ValueError("DeployLocal requires model_path input")

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
                f"DeployLocal could not find model artifact: {source_model_path}"
            )

        deployment_dir = self._prepare_deployment_directory()
        deployed_model_path = self._move_model_artifact(source_model_path, deployment_dir)

        self._write_runtime_assets(deployment_dir=deployment_dir, model_filename=deployed_model_path.name)

        self._ensure_runtime_env(deployment_dir)
        self._start_service(deployment_dir)
        self.finish_execution()

    def _resolve_port(self, port) -> int:
        """Resolves and validates host port, defaulting to 8000."""
        if port in (None, ""):
            return 8000

        resolved = int(port)
        if resolved <= 0:
            raise ValueError("DeployLocal requires a positive port")
        return resolved

    def _prepare_deployment_directory(self) -> SysPath:
        """Ensures artifacts/deployment exists and returns its path."""
        deployment_dir = SysPath.cwd() / "artifacts" / "deployment"
        deployment_dir.mkdir(parents=True, exist_ok=True)
        return deployment_dir

    def _move_model_artifact(self, source_model_path: SysPath, deployment_dir: SysPath) -> SysPath:
        """Moves the serialized model into artifacts/deployment."""
        target_path = deployment_dir / source_model_path.name
        if source_model_path.resolve() == target_path.resolve():
            return target_path
        return SysPath(shutil.move(str(source_model_path), str(target_path)))

    def _write_runtime_assets(self, deployment_dir: SysPath, model_filename: str) -> None:
        """Creates runtime files needed to serve inference locally."""
        config_path = deployment_dir / "deployment_config.json"
        requirements_path = deployment_dir / "requirements.txt"
        service_path = deployment_dir / "service.py"

        config_content = {
            "model_filename": model_filename,
            "model_extension": SysPath(model_filename).suffix.lower(),
            "model_artifact_path": model_filename,
        }
        self._write_json_file(config_path, config_content)

        requirements_content = self._load_deployment_template("requirements.txt.template")
        service_content = self._load_deployment_template("service.py.template")

        requirements_path.write_text(requirements_content, encoding="utf-8")
        service_path.write_text(service_content, encoding="utf-8")

    def _load_deployment_template(self, template_name: str) -> str:
        """Loads a deployment template from package templates directory."""
        template_path = SysPath(__file__).resolve().parent / "templates" / template_name
        if not template_path.exists() or not template_path.is_file():
            raise FileNotFoundError(f"DeployLocal could not find template: {template_path}")
        return template_path.read_text(encoding="utf-8")

    def _ensure_runtime_env(self, deployment_dir: SysPath) -> None:
        """Creates a local venv and installs runtime requirements."""
        venv_dir = deployment_dir / ".venv"
        if not venv_dir.exists():
            self._run_command([sys.executable, "-m", "venv", str(venv_dir)], cwd=deployment_dir)

        pip_path = venv_dir / "bin" / "pip"
        requirements_path = deployment_dir / "requirements.txt"
        self._run_command(
            [str(pip_path), "install", "--no-cache-dir", "-r", str(requirements_path)],
            cwd=deployment_dir,
        )

    def _start_service(self, deployment_dir: SysPath):
        """Starts the FastAPI service in the deployment directory."""
        venv_python = deployment_dir / ".venv" / "bin" / "python"
        env = os.environ.copy()
        env["PORT"] = str(self.port)
        return subprocess.Popen(
            [str(venv_python), "service.py"],
            cwd=str(deployment_dir),
            env=env,
        )

    def _run_command(self, cmd: list[str], cwd: SysPath) -> None:
        """Executes system command and reports stderr on failure."""
        subprocess.run(
            cmd,
            cwd=str(cwd),
            check=True,
            capture_output=True,
            text=True,
        )

    def _write_json_file(self, target_path: SysPath, content: dict) -> None:
        """Writes JSON files using UTF-8 and pretty indentation for readability."""
        with open(target_path, "w", encoding="utf-8") as file_obj:
            json.dump(content, file_obj, ensure_ascii=False, indent=2)
