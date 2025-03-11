import os
import sys
import copy
from common.config import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR, 'src/com/qboson'))
import kaiwu as kw
import numpy as np
from kaiwu.core import (Binary, BinaryExpression, get_min_penalty_from_deltas,
                        get_min_penalty_for_equal_constraint, get_min_penalty)


def find_feasible_solutions(cons: BinaryExpression) -> list:
    """
    返回所有满足cons约束的解（只包含cons中含有的变量）
    :param cons: 线性等式约束：cons=0
    :return: dict组成的list。dict中key为binary变量，value为0或1
    """
    res = list()
    variables = sorted([key[0] for key in cons.coefficient])
    n = len(variables)
    nums = [0 for j in range(n)]
    for i in range(pow(2, n)):
        for j in range(n):
            nums[j] = (i >> j) & 1
        sol = dict(zip(variables, nums))
        if sum([sol[x] * cons.coefficient[(x,)] for x in variables]) == -cons.offset:
            res.append(copy.deepcopy(sol))
    return res


def find_min_constraint_solutions(cons: BinaryExpression) -> list:
    """
    返回所有满足cons约束的解（只包含cons中含有的变量）
    :param cons: 线性等式约束：cons=0
    :return: dict组成的list。dict中key为binary变量，value为0或1
    """
    qubo_model = kw.qubo.QuboModel(cons)
    ising = kw.conversion.qubo_model_to_ising_model(qubo_model)
    mat = ising.get_matrix()

    res = list()
    variables = []
    for var_tuple in cons.coefficient:
        for vari in var_tuple:
            if vari not in variables:
                variables.append(vari)
    variables = sorted(variables)

    n = len(variables)
    nums = [1] * (n + 1)
    best_h = None
    for i in range(pow(2, n)):
        for j in range(n):
            nums[j] = (i >> j) & 1
        sol_dict = dict(zip(variables, nums[:-1]))
        sol = np.array(nums) * 2 - 1
        new_h = -sol.dot(mat).dot(sol)
        if best_h is None or best_h > new_h:
            best_h = new_h
            res = [sol_dict]
        elif best_h == new_h:
            res.append(sol_dict)
    return res


def is_local_optimal_equal_constraint(obj: BinaryExpression, cons: BinaryExpression, penalty, feasible_sol: dict) -> bool:
    """
    判断这个可行解在其邻域内（翻转一个比特的邻域）是不是局部最优的
    :param obj: 原目标函数值
    :param cons: 线性等式约束：cons=0
    :param feasible_sol: 一个满足cons约束的解（只包含cons中含有的变量）key是二值变量，value是0或1
    :return: True表示可行解是局部最优的
    """
    cons_variables = [key[0] for key in cons.coefficient]  # 放约束项cons所包含的所有变量
    obj_variables = set()  # 放目标函数obj所包含的所有变量
    for key in obj.coefficient:
        obj_variables.add(key[0])
        if key[0] not in cons_variables:
            feasible_sol[key[0]] = 1
        if len(key) == 2:
            obj_variables.add(key[1])
    variables = set(cons_variables) & obj_variables
    qubo = obj + penalty * pow(cons, 2)
    return is_local_optimal(qubo, feasible_sol, variables)


def is_local_optimal(qubo, sol, variables):
    the_value = 0
    for k, v in qubo.coefficient.items():
        tmp = v
        for var in k:
            tmp *= sol[var]
        the_value += tmp
    for k in sol:
        if k in variables:
            temp_sol = copy.deepcopy(sol)
            temp_sol[k] = 1 - temp_sol[k]
            temp_value = 0
            for k, v in qubo.coefficient.items():
                tmp = v
                for var in k:
                    tmp *= temp_sol[var]
                temp_value += tmp
            if temp_value < the_value:
                return False
    return True


def test_get_min_penalty_for_equal_constraint():
    x = [Binary("b" + str(i)) for i in range(3)]
    cons = 2 * x[0] - 3 * x[1] + 4 * x[2] - 3
    obj = 2 * x[0] + x[1] + 2 * x[2]

    penalty = get_min_penalty_for_equal_constraint(obj, cons)
    res = find_feasible_solutions(cons)
    for feasible_sol in res:
        assert is_local_optimal_equal_constraint(obj, cons, penalty, feasible_sol) is True
        assert is_local_optimal_equal_constraint(obj, cons, penalty / 10, feasible_sol) is False


def test_get_min_penalty():
    x = [Binary("b" + str(i)) for i in range(4)]
    v = ["bb" + str(i) for i in range(4)]
    cons = (x[0] + x[1] + 2 * x[3] - 2) ** 2 + 2 * x[2]
    obj = 3 * (x[0] - x[1]) ** 2 - 2 * x[2]

    penalty = get_min_penalty(obj, cons)
    res = find_min_constraint_solutions(cons)
    for sol in res:
        assert is_local_optimal(obj + penalty * cons, sol, v) is True
        assert is_local_optimal(obj + penalty / 10 * cons, sol, v) is False


def test_get_min_penalty_exhaustive():
    x = [Binary("b" + str(i)) for i in range(4)]
    v = ["bb" + str(i) for i in range(4)]
    cons = (x[0] + x[1] + 2 * x[3] - 2) ** 2 + 2 * x[2]
    obj = 3 * (x[0] - x[1]) ** 2 - 2 * x[2]

    obj_vars = obj.get_variables()
    neg_delta, pos_delta = obj.get_max_deltas()
    penalty = get_min_penalty_from_deltas(cons, neg_delta, pos_delta, obj_vars, min_delta_method='exhaust')
    res = find_min_constraint_solutions(cons)
    for feasible_sol in res:
        assert is_local_optimal(obj + penalty * cons, feasible_sol, v) is True
        assert is_local_optimal(obj + penalty / 10 * cons, feasible_sol, v) is False
