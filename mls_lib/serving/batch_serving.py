"""Batch Serving: Submits batch prediction jobs to an external model API."""

from __future__ import annotations

import json
import urllib.request
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd

from mls_lib.orchestration.task import Task
from mls_lib.objects.data_frame import DataFrame


class BatchServing(Task):
    """Batch Serving: Submits batch prediction jobs to an external model API."""

    def __init__(self, endpoint_url: str, features_scaler_path: str = None, truth_scaler_path: str = None) -> None:
        super().__init__()
        self.endpoint_url = (endpoint_url or "").strip()
        self.features_scaler_path = (features_scaler_path or "").strip()
        self.truth_scaler_path = (truth_scaler_path or "").strip()
        self.features = DataFrame()

    def set_data(self, features: DataFrame) -> None:
        self.features = features

    def execute(self) -> None:
        if not self.endpoint_url:
            raise ValueError("BatchServing requires endpoint_url")


        features_df = self.features.get_data()

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
        predictions_df = self._normalize_payload(response_json, body)

        if self.truth_scaler_path and not predictions_df.empty:
            truth_scaler = joblib.load(self.truth_scaler_path)
            predictions_df.columns = truth_scaler.columns
            mls_pred = DataFrame()
            mls_pred.set_data(predictions_df)
            truth_scaler.inverse_transform(mls_pred)
            predictions_df = mls_pred.get_data()


        self._write_batch_result(original_features_df, predictions_df)

    def _safe_json_loads(self, body: str):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {"result": body}

    def _write_batch_result(self, original_df: pd.DataFrame, predictions_df: pd.DataFrame) -> None:
        output_dir = Path.cwd() / "serving_results"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"prediction_{timestamp}.csv"

        original_df = original_df.reset_index(drop=True)
        predictions_df = predictions_df.reset_index(drop=True)

        result_df = pd.concat([original_df, predictions_df], axis=1)
        result_df.to_csv(output_path, index=False)

    def _normalize_payload(self, payload, raw_body: str) -> pd.DataFrame:
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

        return pd.DataFrame({"prediction": [raw_body]})
