# tests/test_iris_loader_integration.py
import pytest
from mls_lib.orchestration.task import Task
from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task
from mls_lib.orchestration.task import Task

# Asume que existe IrisDatasetLoader en mls_lib.data_collection
from mls_lib.data_collection.iris_dataset_loader import IrisDatasetLoader

class CountRowsTask(Task):
    def execute(self):
        df = self._get_input("data")
        rows = len(df.data)
        out = DataFrame()
        out.set_data([[rows]])
        self._set_output("n_rows", out)

def test_iris_loader_and_counter():
    loader = IrisDatasetLoader()
    loader.execute()
    data = loader.get_outputs("data")

    counter = CountRowsTask()
    counter.set_inputs({"data": data})
    counter.execute()
    result = counter.get_outputs()["n_rows"]
    assert result.data[0][0] == 150  # Iris dataset has 150 rows
