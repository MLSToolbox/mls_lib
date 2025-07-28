from pytest import fixture
from unittest.mock import patch, Mock
from mls_lib.orchestration import Stage, Task



@fixture
def stage():
    return Stage("empty_stage")

def test_empty_stage(stage: Stage):
    assert stage.name == "empty_stage"
    assert stage.tasks == {}
    assert stage.inputs == {}
    assert stage.outputs == {}
    assert not stage.finished
    assert str(stage) == "empty_stage"

def test_add_task(stage: Stage):
    m = Mock()
    stage.add_task(m, task_name=(stage, "task"))

    task_key = list(stage.tasks.keys())[0]
    assert stage.tasks[task_key] == (m,{"task_name": (stage, "task")})
    assert stage.inputs == {}
    assert stage.outputs == {}
    assert not stage.finished
    assert len(stage.tasks) == 1

    stage.add_task(m, task_name = (m, "task2"))
    
    task_key = list(stage.tasks.keys())[1]
    assert stage.tasks[task_key] == (m, {"task_name": (m, "task2")})
    assert stage.inputs == {}
    assert stage.outputs == {}
    assert not stage.finished
    assert len(stage.tasks) == 2

def test_add_output(stage: Stage):
    m = Mock()
    stage.add_output("task", (m, "task"))
    assert stage.outputs == {"task": (m, "task")}
    assert stage.inputs == {}
    assert not stage.finished
    assert len(stage.outputs) == 1

    stage.add_output("task2", (m, "task2"))
    assert stage.outputs == {"task": (m, "task"), "task2": (m, "task2")}
    assert stage.inputs == {}
    assert not stage.finished
    assert len(stage.outputs) == 2

def test_get_stage_output(stage: Stage):
    m = Mock()
    m.get_output.return_value = "output"
    stage.add_output("task", (m, "task"))
    assert stage.get_stage_output("task") == "output"
    m.get_output.assert_called_once_with("task")

def test_set_data(stage: Stage):
    stage.set_data(a=1, b=2)
    assert stage.inputs == {"a": 1, "b": 2}
    assert stage.outputs == {}
    assert not stage.finished

def test_get_output(stage: Stage):
    stage.set_data(a=1, b=2)
    assert stage.get_output("a") == 1

def test_finish_execution(stage: Stage):
    stage.finish_execution()
    assert stage.finished

def test_execute(stage: Stage):
    m = Mock()
    m.execute.return_value = "output"
    m.is_finished.side_effect = [False, True]
    stage.add_task(m, task_name=(m, "task"))
    stage.add_output("task", (m, "task"))
    stage.execute()
    m.execute.assert_called_once()
    # called 2 times
    assert m.is_finished.call_count == 2
    assert stage.finished