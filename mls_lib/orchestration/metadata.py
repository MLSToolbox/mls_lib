"""Execution metadata helpers for pipeline tasks."""

from copy import deepcopy
from enum import Enum


class Metadata:
    """Shared execution metadata state and operations.

    This class stores runtime metadata while a pipeline executes.
    It exposes helper methods so tasks can append data-cleaning information.
    """

    class DataCleaningOperation(str, Enum):
        """Operations for system's data cleaning steps, used in metadata entries."""

        REPLACE_NULL_AVERAGE = "replace_null_average"
        REPLACE_NULL_MEDIAN = "replace_null_median"
        REPLACE_NULL_MODE = "replace_null_mode"
        REPLACE_NULL_TEXT = "replace_null_text"
        REPLACE_NULL_ZERO = "replace_null_zero"
        REPLACE_VALUE = "replace_value"
        JOIN_DATA_FRAME = "join_data_frame"

    _STATE = {
        "schema_version": "1.0.0",
        "data_cleaning": [],
    }

    @classmethod
    def resetMetadata(cls) -> None:
        """Resets metadata state for each pipeline execution.

        Called before a pipeline run starts, so metadata from previous runs
        is not mixed with the current one.
        """
        cls._STATE["schema_version"] = "1.0.0"
        cls._STATE["data_cleaning"] = []

    @classmethod
    def addDataCleaningEntry(
        cls,
        operation: "Metadata.DataCleaningOperation",
        columns: list[str],
        replacement_values: list | None = None,
    ) -> None:
        """Adds one data-cleaning operation entry.

        Each entry stores operation type and the values needed to replay or
        understand how columns were transformed.
        """
        entry = {
            "type": operation.value,
            "columns": [str(column) for column in columns],
            "replacement_values": replacement_values or [],
        }

        if entry not in cls._STATE["data_cleaning"]:
            cls._STATE["data_cleaning"].append(entry)

    @classmethod
    def getMetadata(cls) -> dict:
        """Returns a deep copy of current metadata.

        Returning a copy prevents accidental mutation of internal state.
        """
        return deepcopy(cls._STATE)
