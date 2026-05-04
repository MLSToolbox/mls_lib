import sys
from pathlib import Path

from mls_lib.deployment import DeployLocal
from mls_lib.objects.path import Path as PathOutput


class DummyProcess:
    def __init__(self, pid: int) -> None:
        self.pid = pid


class TestDeployLocal:
    def test_deploys_model_and_starts_service(self, tmp_path, monkeypatch):
        """Should move model into artifacts/deployment and start the local service."""
        monkeypatch.chdir(tmp_path)

        artifacts_dir = tmp_path / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        source_model_path = artifacts_dir / "trained_model.joblib"
        source_model_path.write_text("serialized-model", encoding="utf-8")

        captured_runs = []
        captured_popen = []

        def _fake_run(cmd, cwd, check, capture_output, text):
            captured_runs.append(
                {
                    "cmd": cmd,
                    "cwd": cwd,
                    "check": check,
                    "capture_output": capture_output,
                    "text": text,
                }
            )

        def _fake_popen(cmd, cwd, env):
            captured_popen.append(
                {
                    "cmd": cmd,
                    "cwd": cwd,
                    "env": env,
                }
            )
            return DummyProcess(pid=4321)

        monkeypatch.setattr("mls_lib.deployment.deploy_local.subprocess.run", _fake_run)
        monkeypatch.setattr("mls_lib.deployment.deploy_local.subprocess.Popen", _fake_popen)

        task = DeployLocal(port="")
        task.set_data(PathOutput(str(source_model_path)))
        task.execute()

        deployment_dir = tmp_path / "artifacts" / "deployment"
        deployed_model_path = deployment_dir / source_model_path.name

        assert deployed_model_path.exists()
        assert not source_model_path.exists()
        assert (deployment_dir / "deployment_config.json").exists()
        assert (deployment_dir / "requirements.txt").exists()
        assert (deployment_dir / "service.py").exists()

        venv_dir = deployment_dir / ".venv"
        assert captured_runs[0]["cmd"][:3] == [sys.executable, "-m", "venv"]
        assert captured_runs[0]["cmd"][3] == str(venv_dir)

        assert captured_runs[1]["cmd"][:4] == [
            str(venv_dir / "bin" / "pip"),
            "install",
            "--no-cache-dir",
            "-r",
        ]
        assert captured_runs[1]["cmd"][4] == str(deployment_dir / "requirements.txt")

        assert captured_popen[0]["cmd"] == [
            str(venv_dir / "bin" / "python"),
            "service.py",
        ]
        assert captured_popen[0]["cwd"] == str(deployment_dir)
        assert captured_popen[0]["env"]["PORT"] == "8000"
