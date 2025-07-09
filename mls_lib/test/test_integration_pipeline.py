# tests/test_pipeline_integration.py
import pytest
from mls_lib.orchestration.task import Task
from mls_lib.objects.data_frame import DataFrame

class GenTask(Task):
    def execute(self):
        df = DataFrame()
        df.set_data([[1, 2, 3]])
        self._set_output("data", df)

class SumTask(Task):
    def execute(self):
        inp = self._get_input("data")
        arr = inp.data[0]
        result = sum(arr)
        out = DataFrame()
        out.set_data([[result]])
        self._set_output("sum", out)

def test_pipeline_sum():
    t1 = GenTask()
    t2 = SumTask()

    t1.execute()
    data = t1.get_outputs("data")
    t2.set_inputs({"data": data})
    t2.execute()

    sum_df = t2.get_outputs("sum")
    assert sum_df.data == [[6]]
