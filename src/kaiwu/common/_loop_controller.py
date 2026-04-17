# -*- coding: utf-8 -*-
"""
循环控制器等一些辅助求解工具
"""
import time
import math
from ._json_serializable_mixin import JsonSerializableMixin


class BaseTimer:
    """计时器"""

    def __init__(self):
        self.prev_time = time.time()
        self.cpu_time = 0
        self.subqubo_time = 0

    def add_to_cpu_time(self):
        """把计时加到cpu时间并更新prev_time"""
        cur_time = time.time()
        self.cpu_time += cur_time - self.prev_time
        self.prev_time = cur_time

    def reset(self):
        """重置时间"""
        self.prev_time = time.time()
        self.cpu_time = 0
        self.subqubo_time = 0


class BaseLoopController(JsonSerializableMixin):
    """循环控制器，并计算时间。用于调试和测试算法

    Args:
        max_repeat_step: 最大步数，默认值为math.inf

        target_objective：目标优化函数，达到即停止，默认值为-math.inf

        no_improve_limit：收敛条件，指定更新次数没有改进则停止，默认值为math.inf

        iterate_per_update：每次更新哈密顿量前运行的次数，默认值为5
    """

    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        max_repeat_step=math.inf,
        target_objective=-math.inf,
        no_improve_limit=math.inf,
        iterate_per_update=5,
    ):
        # 判断步数
        self.repeat_step = 0
        self.max_repeat_step = max_repeat_step
        # 判断目标函数
        self.prev_objective = math.inf
        self.target_objective = target_objective
        # 判断收敛
        self.pass_count = 0
        self.no_improve_limit = no_improve_limit

        self.iterate_step = 0
        self.iterate_per_update = iterate_per_update
        self.unsatisfied_constraints_count = None
        if all(
            v == math.inf
            for v in (
                self.max_repeat_step,
                self.target_objective,
                self.no_improve_limit,
            )
        ):
            raise ValueError(
                "At least one termination condition must be set "
                "(max_repeat_step, target_objective, or no_improve_limit)"
            )
        self.timer = BaseTimer()

    def update_status(self, objective, unsatisfied_constraints_count=None):
        """在计算子问题后更新状态

        Args:
            objective (float): 目标函数值

            unsatisfied_constraints_count (int): 未满足约束项的数量
        """
        self.unsatisfied_constraints_count = unsatisfied_constraints_count
        if objective is not None and objective < self.prev_objective:
            self.prev_objective = objective
            self.pass_count = 0
        else:
            self.pass_count += 1
        self.repeat_step += 1

    def is_finished(self):
        """判断是否应该停止

        Returns:
            bool: 是否应该停止
        """
        finish = False
        if self.prev_objective <= self.target_objective and (
            self.unsatisfied_constraints_count is None
            or self.unsatisfied_constraints_count == 0
        ):
            finish = True
        if self.pass_count >= self.no_improve_limit:
            finish = True
        if self.repeat_step >= self.max_repeat_step:
            finish = True
        return finish

    def restart(self):
        """重新初始化计数"""
        self.repeat_step = 0
        self.prev_objective = math.inf
        self.pass_count = 0
        self.timer.reset()

    def to_json_dict(self, exclude_fields=("timer",)):
        """转化为json字典

        Returns:
            dict: json字典
        """
        return super().to_json_dict(exclude_fields=exclude_fields)


class OptimizerLoopController(BaseLoopController):
    """Optimizer循环控制器，并计算时间。用于调试和测试算法

    Args:
        max_repeat_step: 最大步数，默认值为math.inf

        target_objective：目标优化函数，达到即停止，默认值为-math.inf

        no_improve_limit：收敛条件，指定更新次数没有改进则停止，默认值为20000

        iterate_per_update：每次更新哈密顿量前运行的次数，默认值为5
    """

    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        max_repeat_step=math.inf,
        target_objective=-math.inf,
        no_improve_limit=20000,
        iterate_per_update=5,
    ):
        # 判断步数
        super().__init__(
            max_repeat_step, target_objective, no_improve_limit, iterate_per_update
        )


class SolverLoopController(BaseLoopController, JsonSerializableMixin):
    """Solver循环控制器，并计算时间。用于调试和测试算法

    Args:
        max_repeat_step (int): 最大步数，默认值为math.inf

        target_objective (float): 目标优化函数，达到即停止，默认值为-math.inf

        no_improve_limit (int): 收敛条件，指定更新次数没有改进则停止，默认值为20000

        iterate_per_update (int): 每次更新哈密顿量前运行的次数，默认值为5

        stop_after_feasible_count (int): 找到指定数量的可行解后停止
    """

    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        max_repeat_step=math.inf,
        target_objective=-math.inf,
        no_improve_limit=math.inf,
        iterate_per_update=5,
        stop_after_feasible_count=None,
    ):
        # 判断步数
        super().__init__(
            max_repeat_step, target_objective, no_improve_limit, iterate_per_update
        )
        self.stop_after_feasible_count = stop_after_feasible_count
        self.feasible_count = 0

    def update_status(self, objective, unsatisfied_constraints_count=None):
        """在计算子问题后更新状态

        Args:
            objective (float): 目标函数值

            unsatisfied_constraints_count (int): 未满足约束项的数量
        """

        super().update_status(objective, unsatisfied_constraints_count)
        if unsatisfied_constraints_count == 0:
            self.feasible_count += 1

    def is_finished(self):
        """判断是否应该停止

        Returns:
            bool: 是否应该停止
        """

        return super().is_finished() or (
            self.stop_after_feasible_count is not None
            and self.feasible_count == self.stop_after_feasible_count
        )
