"""Tests for loop controller timing, termination, and serialization behavior."""

import math

import pytest

from kaiwu.common import BaseLoopController, OptimizerLoopController, SolverLoopController
from kaiwu.common._loop_controller import BaseTimer


def test_base_timer_adds_elapsed_time_and_resets(monkeypatch):
    # Pin time.time so elapsed-time and reset behavior are deterministic.
    times = iter([10.0, 12.5, 20.0])
    monkeypatch.setattr("kaiwu.common._loop_controller.time.time", lambda: next(times))
    timer = BaseTimer()

    timer.add_to_cpu_time()
    timer.subqubo_time = 3
    timer.reset()

    assert timer.cpu_time == 0
    assert timer.subqubo_time == 0
    assert timer.prev_time == 20.0


def test_base_loop_controller_requires_a_termination_condition():
    with pytest.raises(ValueError, match="At least one termination condition"):
        BaseLoopController(
            max_repeat_step=math.inf,
            target_objective=math.inf,
            no_improve_limit=math.inf,
        )


def test_base_loop_controller_tracks_improvement_and_no_improvement_limit():
    controller = BaseLoopController(max_repeat_step=10, no_improve_limit=2)

    controller.update_status(5)
    controller.update_status(6)
    assert not controller.is_finished()

    # None is treated as no improvement and contributes to pass_count.
    controller.update_status(None)
    assert controller.is_finished()
    assert controller.prev_objective == 5
    assert controller.pass_count == 2
    assert controller.repeat_step == 3


def test_base_loop_controller_finishes_at_target_only_when_constraints_satisfied():
    controller = BaseLoopController(max_repeat_step=10, target_objective=3)

    controller.update_status(2, unsatisfied_constraints_count=1)
    assert not controller.is_finished()

    # Target objective is enough only after all constraints are satisfied.
    controller.update_status(2, unsatisfied_constraints_count=0)
    assert controller.is_finished()


def test_base_loop_controller_restart_resets_progress_but_keeps_limits():
    controller = BaseLoopController(max_repeat_step=2)
    controller.update_status(4)
    controller.update_status(4)
    assert controller.is_finished()

    controller.restart()

    assert not controller.is_finished()
    assert controller.repeat_step == 0
    assert controller.pass_count == 0
    assert controller.prev_objective == math.inf
    assert controller.max_repeat_step == 2


def test_base_loop_controller_json_excludes_timer_by_default():
    controller = BaseLoopController(max_repeat_step=1, iterate_per_update=3)

    json_dict = controller.to_json_dict()

    # Runtime timer state is intentionally not persisted by default.
    assert "timer" not in json_dict
    assert json_dict["max_repeat_step"] == 1
    assert json_dict["iterate_per_update"] == 3


def test_optimizer_loop_controller_default_no_improve_limit():
    controller = OptimizerLoopController(max_repeat_step=math.inf)

    assert controller.no_improve_limit == 20000


def test_solver_loop_controller_stops_after_feasible_count():
    controller = SolverLoopController(
        max_repeat_step=math.inf,
        no_improve_limit=math.inf,
        stop_after_feasible_count=2,
    )

    controller.update_status(5, unsatisfied_constraints_count=0)
    assert not controller.is_finished()

    # SolverLoopController adds a feasible-solution count termination condition.
    controller.update_status(4, unsatisfied_constraints_count=0)
    assert controller.is_finished()
    assert controller.feasible_count == 2
