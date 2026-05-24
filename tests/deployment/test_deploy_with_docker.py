from pathlib import Path

from mls_lib.deployment import DeployWithDocker
from mls_lib.objects.path import Path as PathOutput


class TestDeployWithDocker:
    def test_deploys_model_path_and_uses_default_port(self, tmp_path, monkeypatch):
        """Should deploy build assets into artifacts/deployment and keep the model in artifacts."""
        monkeypatch.chdir(tmp_path)

        artifacts_dir = tmp_path / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        source_model_path = artifacts_dir / "trained_model.joblib"
        source_model_path.write_text("serialized-model", encoding="utf-8")


        captured_commands = []

        def _fake_run(cmd, cwd, check, capture_output, text):
            captured_commands.append(
                {
                    "cmd": cmd,
                    "cwd": cwd,
                    "check": check,
                    "capture_output": capture_output,
                    "text": text,
                }
            )

        monkeypatch.setattr("mls_lib.deployment.deploy_with_docker.subprocess.run", _fake_run)

        task = DeployWithDocker(
            image_name="demo-image",
            port="",
        )
        task.set_data(PathOutput(str(source_model_path)))
        task.execute()

        deployment_dir = tmp_path / "artifacts" / "deployment"
        assert source_model_path.exists()
        assert (deployment_dir / "deployment_config.json").exists()
        assert (deployment_dir / "Dockerfile").exists()
        assert (deployment_dir / "requirements.txt").exists()
        assert (deployment_dir / "service.py").exists()

        assert len(captured_commands) == 3
        assert captured_commands[0]["cmd"][:6] == [
            "docker",
            "build",
            "-f",
            str(deployment_dir / "Dockerfile"),
            "--build-arg",
            f"MODEL_FILENAME={source_model_path.name}",
        ]
        assert captured_commands[0]["cmd"][6:8] == ["-t", "demo-image"]
        assert captured_commands[0]["cmd"][-1] == "."
        assert captured_commands[0]["cwd"] == str(tmp_path)
        assert captured_commands[1]["cmd"] == ["docker", "rm", "-f", "demo-image"]
        assert captured_commands[1]["cwd"] == str(tmp_path)
        assert captured_commands[2]["cmd"][:7] == [
            "docker",
            "run",
            "-d",
            "--name",
            "demo-image",
            "-p",
            "8000:8000",
        ]
        assert captured_commands[2]["cmd"][7:9] == ["-e", "PORT=8000"]
        assert captured_commands[2]["cmd"][-1] == "demo-image"
        assert captured_commands[2]["cwd"] == str(tmp_path)

    def test_deploys_string_model_path_already_in_artifacts(self, tmp_path, monkeypatch):
        """Should deploy model path already prepared in artifacts when input is a PathOutput."""
        monkeypatch.chdir(tmp_path)

        artifacts_dir = tmp_path / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        external_artifact = artifacts_dir / "external_model.onnx"
        external_artifact.write_text("onnx-binary-content", encoding="utf-8")

        captured_commands = []

        def _fake_run(cmd, cwd, check, capture_output, text):
            captured_commands.append(
                {
                    "cmd": cmd,
                    "cwd": cwd,
                    "check": check,
                    "capture_output": capture_output,
                    "text": text,
                }
            )

        monkeypatch.setattr("mls_lib.deployment.deploy_with_docker.subprocess.run", _fake_run)

        task = DeployWithDocker(
            image_name="external-image",
            port=9010,
        )
        task.set_data(PathOutput(str(external_artifact)))
        task.execute()

        deployment_dir = tmp_path / "artifacts" / "deployment"
        assert (deployment_dir / "deployment_config.json").exists()
        assert (deployment_dir / "Dockerfile").exists()
        assert (deployment_dir / "requirements.txt").exists()
        assert (deployment_dir / "service.py").exists()
        assert external_artifact.exists()

        assert len(captured_commands) == 3
        assert captured_commands[0]["cmd"][:6] == [
            "docker",
            "build",
            "-f",
            str(deployment_dir / "Dockerfile"),
            "--build-arg",
            f"MODEL_FILENAME={external_artifact.name}",
        ]
        assert captured_commands[0]["cmd"][6:8] == ["-t", "external-image"]
        assert captured_commands[0]["cmd"][-1] == "."
        assert captured_commands[0]["cwd"] == str(tmp_path)
        assert captured_commands[1]["cmd"] == ["docker", "rm", "-f", "external-image"]
        assert captured_commands[1]["cwd"] == str(tmp_path)
        assert captured_commands[2]["cmd"][:7] == [
            "docker",
            "run",
            "-d",
            "--name",
            "external-image",
            "-p",
            "9010:9010",
        ]
        assert captured_commands[2]["cmd"][7:9] == ["-e", "PORT=9010"]
        assert captured_commands[2]["cmd"][-1] == "external-image"
        assert captured_commands[2]["cwd"] == str(tmp_path)
