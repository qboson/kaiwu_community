自定义求解器与优化器
================================

本章节将介绍如何在Kaiwu SDK社区版中创建自定义的求解器（solver）和优化器（optimizer），帮助您扩展SDK的求解能力。

概述
----

Kaiwu Community 提供了灵活的优化器（Optimizer）和求解器（Solver）抽象类，使用户可以基于框架扩展自定义算法。

在 Kaiwu Community 中:

* Optimizer：用于执行具体解算过程（例如模拟退火、禁忌搜索、量子优化器等）。
* Solver：负责接收 QUBO 模型，将其传给 Optimizer 并收集结果，同时处理约束等高级逻辑。

两者解耦，使得开发者可以专注实现优化方法，而不用关心 QUBO 建模、验证等通用逻辑。

自定义优化器
------------

OptimizerBase 简介
^^^^^^^^^^^^^^^^^^^^^^^^

优化器需要继承`kaiwu_community.core.OptimizerBase`类，并实现以下方法：

- `__init__`：初始化优化器，设置参数
- `solve`：执行优化算法，返回最优解

基本代码结构如下：

.. code:: python

    import math
    import numpy as np
    from kaiwu_community.core import OptimizerBase

    class BruteForceOptimizer(OptimizerBase):
        """A brute force solver for the Ising model matrix, which is slow but accurate"""
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Initialize custom parameters

        def solve(self, ising_matrix=None):
            """Solve Ising matrix with solve interface

            Args:
                ising_matrix (np.ndarray, optional): Ising Matrix. Defaults to None.

            Returns:
                np.ndarray: One or multiple solution vectors with the lowest energy.

            Examples:
                >>> import kaiwu_community as kw
                >>> import numpy as np
                >>> mat = np.array([[0, 2, -3],[2, 0, -1],[-3, -1, 0]])
                >>> optimizer = kw.classical.BruteForceOptimizer()
                >>> optimizer.solve(mat)
                array([[-1, -1,  1],
                       [-1, -1,  1]])

            """
            size = ising_matrix.shape[0]
            h_ret = math.inf
            solutions = []
            for i in range(2 ** size):
                val = i
                vlist = [0] * size
                for j in range(size):
                    vlist[j] = val % 2
                    val //= 2
                sol = np.array(vlist) * 2 - 1
                hmt = -sol.dot(ising_matrix).dot(sol)
                if hmt < h_ret:
                    h_ret = hmt
                    solutions = [sol]
                elif hmt == h_ret:
                    solutions.append(sol)
            sols = np.array(solutions)
            sols[sols[:, -1] <= 0, :] *= -1
            return sols

说明
^^^^^^^^^^

* ising_matrix 是从 QUBO 模型转换而来的 Ising 格式矩阵。

* 返回结果是一个只包含-1和1的ndarray，是 Ising 矩阵的解向量。

自定义求解器
---------------

SolverBase 简介
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Solver 是封装优化器运行逻辑的基类，负责：

1. 调用 Optimizer 求解；
2. 将 QUBO 模型转换为 Ising 矩阵；
3. 返回最终解和目标值。

自定义 Solver 继承自 SolverBase：

.. code:: python

    from kaiwu_community.core import get_sol_dict
    from kaiwu_community.conversion import qubo_model_to_ising_model
    from kaiwu_community.core import SolverBase
    from kaiwu_community.common import hamiltonian

    def _to_ising_matrix(qubo_model):
        ising_model = qubo_model_to_ising_model(qubo_model)
        ising_mat = ising_model.get_matrix()
        bias = ising_model.get_bias()
        vars_dict = ising_model.get_variables()
        return ising_mat, bias, vars_dict


    class SimpleSolver(SolverBase):
        """Implement direct solving of QuboModel using Optimizer

        Examples:
            >>> import kaiwu_community as kw
            >>> n = 10
            >>> W = 5
            >>> p = [i + 1 for i in range(n)]
            >>> w = [(i + 2) / 2 for i in range(n)]
            >>> x = kw.core.ndarray(n, 'x', kw.core.Binary)
            >>> qubo_model = kw.qubo.QuboModel()
            >>> qubo_model.set_objective(sum(x[i] * p[i] * (-1) for i in range(n)))
            >>> qubo_model.add_constraint(sum(x[i] * w[i] for i in range(n)) <= W, "c", penalty=10)
            >>> solver = kw.solver.SimpleSolver(kw.classical.BruteForceOptimizer())
            >>> sol_dict, qubo_val = solver.solve_qubo(qubo_model)
            >>> unsatisfied_count, result_dict = qubo_model.verify_constraint(sol_dict)
            >>> unsatisfied_count
            0

        Returns:
            tuple: Result dictionary and Result dictionary.

            - dict: Result dictionary. The key is the variable name, and the value is the corresponding spin value.

            - float: qubo value.
        """

        def solve_qubo(self, qubo_model):
            ising_mat, bias, vars_dict = _to_ising_matrix(qubo_model)
            solutions = self._optimizer.solve(ising_mat)
            if solutions is None:
                return None, None
            solution_dicts = get_sol_dict(solutions[0][:-1] * solutions[0][-1], vars_dict)
            return solution_dicts, hamiltonian(ising_mat, solutions)[0] + bias

说明
^^^^^^^^^^

* _to_ising_matrix() 将 QUBO 表达式转换为对应的 Ising 矩阵；
* _optimizer 是传入的优化器实例；
* solve_qubo 应返回解和目标值。

完整示例
--------

以下是一个完整的示例，展示如何创建和使用自定义优化器和求解器：

.. code:: python

    import math
    import numpy as np
    import kaiwu_community as kw
    from kaiwu_community.core import OptimizerBase, SolverBase
    from kaiwu_community.core import get_sol_dict
    from kaiwu_community.conversion import qubo_model_to_ising_model
    from kaiwu_community.core import SolverBase
    from kaiwu_community.common import hamiltonian


    class CustomOptimizer(OptimizerBase):
        def solve(self, ising_matrix=None):

            size = ising_matrix.shape[0]
            h_ret = math.inf
            solutions = []
            for i in range(2 ** size):
                val = i
                vlist = [0] * size
                for j in range(size):
                    vlist[j] = val % 2
                    val //= 2
                sol = np.array(vlist) * 2 - 1
                hmt = -sol.dot(ising_matrix).dot(sol)
                if hmt < h_ret:
                    h_ret = hmt
                    solutions = [sol]
                elif hmt == h_ret:
                    solutions.append(sol)
            sols = np.array(solutions)
            sols[sols[:, -1] <= 0, :] *= -1
            return sols


    def _to_ising_matrix(qubo_model):
        ising_model = qubo_model_to_ising_model(qubo_model)
        ising_mat = ising_model.get_matrix()
        bias = ising_model.get_bias()
        vars_dict = ising_model.get_variables()
        return ising_mat, bias, vars_dict


    class CustomSolver(SolverBase):

        def solve_qubo(self, qubo_model):
            ising_mat, bias, vars_dict = _to_ising_matrix(qubo_model)
            solutions = self._optimizer.solve(ising_mat)
            if solutions is None:
                return None, None
            solution_dicts = get_sol_dict(solutions[0][:-1] * solutions[0][-1], vars_dict)
            return solution_dicts, hamiltonian(ising_mat, solutions)[0] + bias


    n = 10
    W = 5
    p = [i + 1 for i in range(n)]
    w = [(i + 2) / 2 for i in range(n)]
    x = kw.core.ndarray(n, 'x', kw.core.Binary)
    qubo_model = kw.qubo.QuboModel()
    qubo_model.set_objective(sum(x[i] * p[i] * (-1) for i in range(n)))
    qubo_model.add_constraint(sum(x[i] * w[i] for i in range(n)) <= W, "c", penalty=10)
    solver = CustomSolver(CustomOptimizer())
    sol_dict, qubo_val = solver.solve_qubo(qubo_model)
    unsatisfied_count, result_dict = qubo_model.verify_constraint(sol_dict)
    print(f"unsatisfied_count: {unsatisfied_count}")


测试与验证
----------

创建自定义求解器和优化器后，您应该对其进行测试和验证，确保它们能够正确工作：

1. **单元测试**：为自定义优化器和求解器编写单元测试
2. **集成测试**：测试它们与现有SDK组件的兼容性
3. **性能测试**：评估它们在不同规模问题上的性能
4. **正确性验证**：使用已知最优解的问题验证求解结果

最佳实践
--------

1. **继承基类**：始终继承SDK提供的基类（如`OptimizerBase`和`SolverBase`），确保兼容性
2. **清晰的文档**：为自定义组件编写详细的文档字符串
3. **参数化设计**：允许通过参数配置优化器的行为
4. **错误处理**：添加适当的错误处理和日志记录
5. **模块化设计**：将复杂功能拆分为多个小模块
6. **遵循命名规范**：使用清晰、一致的命名规范
7. **测试覆盖**：编写全面的测试用例
8. **性能优化**：针对大规模问题优化算法性能

总结
----

本章节介绍了如何在Kaiwu SDK社区版中创建自定义的求解器和优化器。通过继承基类并实现必要的方法，您可以轻松扩展SDK的求解能力，适应不同的问题需求。

创建自定义求解器和优化器是扩展Kaiwu SDK功能的重要方式，希望本教程能够帮助您快速上手。如果您有任何问题或建议，欢迎通过GitHub Issues提交。
