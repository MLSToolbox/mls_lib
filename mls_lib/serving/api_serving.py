"""API Serving: Calls an external model endpoint for real-time prediction."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Any

import pandas as pd

import joblib

from mls_lib.orchestration.task import Task
from mls_lib.objects.data_frame import DataFrame


class ApiServing(Task):
    """API Serving: Calls an external model endpoint for real-time prediction."""

    def __init__(self, endpoint_url: str, output_path: str, features_scaler_path: str = None, truth_scaler_path: str = None) -> None:
        super().__init__()
        self.endpoint_url = (endpoint_url or "").strip()
        self.output_path = (output_path or "").strip()
        self.features_scaler_path = (features_scaler_path or "").strip()
        self.truth_scaler_path = (truth_scaler_path or "").strip()
        self.features = DataFrame()

    def set_data(self, features: DataFrame) -> None:
        self.features = features

    def execute(self) -> None:
        if not self.endpoint_url:
            raise ValueError("ApiServing requires endpoint_url")
        if not self.output_path:
            raise ValueError("ApiServing requires output_path")

        features_df = self._resolve_features()

        original_features_df = features_df.copy()

        if self.features_scaler_path:
            feature_scaler = joblib.load(self.features_scaler_path)
            mls_df = DataFrame()
            mls_df.set_data(features_df)
            feature_scaler.transform(mls_df)
            features_df = mls_df.get_data()


        inputs = features_df.to_numpy().tolist()
        payload = json.dumps({"inputs": inputs}).encode("utf-8")

        request = urllib.request.Request(
            self.endpoint_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")

        response_json = self._safe_json_loads(body)
        predictions_df = self._normalize_predictions(response_json)

        if self.truth_scaler_path and not predictions_df.empty:
            truth_scaler = joblib.load(self.truth_scaler_path)
            predictions_df.columns = truth_scaler.columns
            mls_pred = DataFrame()
            mls_pred.set_data(predictions_df)
            truth_scaler.inverse_transform(mls_pred)
            predictions_df = mls_pred.get_data()

        self._write_result(original_features_df, predictions_df)

    def _resolve_features(self) -> pd.DataFrame:
        features_df = self.features.get_data()
        if features_df is None:
            raise ValueError("ApiServing requires features input")
        if len(features_df) != 1:
            raise ValueError("ApiServing expects a single row of features")
        return features_df

    def _safe_json_loads(self, body: str) -> Any:
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {"prediction": [body]}

    def _normalize_predictions(self, payload: Any) -> pd.DataFrame:
        data = payload
        if isinstance(payload, dict):
            if "predictions" in payload:
                data = payload["predictions"]
            elif "result" in payload:
                data = payload["result"]

        if isinstance(data, list):
            if len(data) == 0:
                return pd.DataFrame()
            if isinstance(data[0], dict):
                return pd.DataFrame(data)
            return pd.DataFrame({"prediction": data})

        if isinstance(data, dict):
            return pd.DataFrame([data])

        return pd.DataFrame({"prediction": [data]})

    def _write_result(self, features_df: pd.DataFrame, predictions_df: pd.DataFrame) -> None:
        output_path = Path(self.output_path)
        if output_path.parent:
            output_path.parent.mkdir(parents=True, exist_ok=True)

        features_payload = features_df.iloc[0].to_dict()
        prediction_payload = self._prediction_payload(predictions_df)
        result = {
            "features": features_payload,
            "truth_column": prediction_payload,
        }

        output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _prediction_payload(self, predictions_df: pd.DataFrame) -> Any:
        if predictions_df.empty:
            return None
        row = predictions_df.iloc[0].to_dict()
        if len(row) == 1:
            return next(iter(row.values()))
        return row