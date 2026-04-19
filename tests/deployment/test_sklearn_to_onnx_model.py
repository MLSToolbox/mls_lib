import pytest

from sklearn.linear_model import LinearRegression

from mls_lib.deployment import SklearnToOnnxModel
from mls_lib.objects.data_frame import DataFrame
from mls_lib.objects.models import LinearRegressionModel


class TestSklearnToOnnxModel:
    @pytest.fixture(autouse=True)
    def _require_skl2onnx(self):
        # Skip the suite if conversion dependency is not present.
        pytest.importorskip("skl2onnx")

    def _build_features(self):
        # This sample data is only used to infer input tensor shape for ONNX.
        features = DataFrame()
        features.from_np_array(
            data=[[1.0, 10.0], [2.0, 20.0], [3.0, 30.0], [4.0, 40.0]],
            headers=["f1", "f2"],
        )
        return features

    def test_execute_converts_wrapped_sklearn_model_to_onnx(self):
        # Project trainers usually output wrapper objects around sklearn estimators.
        # This verifies converter unwrapping + conversion path.
        wrapped_model = LinearRegressionModel()
        wrapped_model.model.fit(
            [[1.0, 10.0], [2.0, 20.0], [3.0, 30.0], [4.0, 40.0]],
            [1.0, 2.0, 3.0, 4.0],
        )

        task = SklearnToOnnxModel()
        task.set_data(model=wrapped_model, features=self._build_features())
        task.execute()

        onnx_model = task.get_output("model")
        assert onnx_model.__class__.__name__ == "ModelProto"

    def test_execute_passes_through_when_model_is_already_onnx(self):
        # Converter should be idempotent if upstream already produced ONNX.
        import onnx

        existing = onnx.ModelProto()
        task = SklearnToOnnxModel()
        task.set_data(model=existing, features=self._build_features())
        task.execute()

        assert task.get_output("model") is existing

    def test_execute_raises_when_features_are_missing(self):
        # For sklearn conversion, input feature width is mandatory.
        estimator = LinearRegression().fit(
            [[1.0, 10.0], [2.0, 20.0], [3.0, 30.0], [4.0, 40.0]],
            [1.0, 2.0, 3.0, 4.0],
        )

        task = SklearnToOnnxModel()
        task.set_data(model=estimator, features=DataFrame())

        with pytest.raises(ValueError, match="requires non-empty features"):
            task.execute()
