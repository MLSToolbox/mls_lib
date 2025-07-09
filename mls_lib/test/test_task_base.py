# tests/test_task_base.py
import pytest
from mls_lib.orchestration.task import Task
from mls_lib.objects.data_frame import DataFrame

class DummyTask(Task):
    def execute(self):
        df = DataFrame()
        df.set_data([[42]])
        self._set_output("out", df)

def test_dummy_task_outputs():
    t = DummyTask()
    t.execute()
    outputs = t.get_outputs()
    assert "out" in outputs
    assert isinstance(outputs["out"], DataFrame)
    assert outputs["out"].data == [[42]]
