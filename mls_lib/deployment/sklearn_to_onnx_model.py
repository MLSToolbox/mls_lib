"""Sklearn to ONNX conversion task."""

from mls_lib.objects.models.model import Model
from mls_lib.orchestration.task import Task
from mls_lib.objects.data_frame import DataFrame

import onnx


class SklearnToOnnxModel(Task):
    """Converts a trained sklearn model into an ONNX ModelProto."""

    def __init__(self) -> None:
        super().__init__()
        self.model = Model()
        self.features = DataFrame()

    def set_data(self, model, features) -> None:
        """Stores model and feature sample used to infer ONNX input shape."""
        # model: trained estimator (or mls_lib wrapper around it)
        # features: sample input used to infer the ONNX input tensor width
        self.model = model
        self.features = features

    def _unwrap_model(self, model):
        # Training tasks in this project often return wrappers with .model inside.
        # The converter needs the raw estimator instance.
        if hasattr(model, "model") and getattr(model, "model") is not None:
            return getattr(model, "model")
        return model

    def getNFeatures(self, features) -> int:
        # Accept mls_lib DataFrame and also plain dataframe-like objects for flexibility.
        if hasattr(features, "get_data"):
            feature_data = features.get_data()
        else:
            feature_data = features

        if feature_data is None:
            raise ValueError("SklearnToOnnxModel requires non-empty features to infer input shape")

        if not hasattr(feature_data, "shape") or len(feature_data.shape) < 2:
            raise ValueError("SklearnToOnnxModel expected 2D features with a valid shape")

        n_features = int(feature_data.shape[1])
        if n_features <= 0:
            raise ValueError("SklearnToOnnxModel inferred an invalid number of features")
        return n_features

    def _get_stable_opset(self) -> int:
        # Use a broadly supported stable opset while respecting runtime maximum.
        max_runtime_opset = int(onnx.defs.onnx_opset_version())
        return min(17, max_runtime_opset)

    def execute(self):
        # Local import keeps this task isolated from environments that do not
        # use ONNX conversion.
        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import FloatTensorType

        model_to_convert = self._unwrap_model(self.model)
        if model_to_convert is None:
            raise ValueError("SklearnToOnnxModel requires a model input")

        if isinstance(model_to_convert, onnx.ModelProto):
            # If a previous step already converted the model, pass it through.
            self._set_output("model", model_to_convert)
            return

        n_features = self.getNFeatures(self.features)
        # ONNX needs an explicit input signature; we infer only feature width here.
        onnx_model = convert_sklearn(
            model_to_convert,
            initial_types=[("input", FloatTensorType([None, n_features]))],
            target_opset=self._get_stable_opset(),
        )

        self._set_output("model", onnx_model)
