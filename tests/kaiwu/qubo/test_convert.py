import os
import sys
import numpy as np
from common.config import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
import kaiwu_community as kw
from kaiwu_community.qubo import qubo_matrix_to_qubo_model
from kaiwu_community.conversion import qubo_matrix_to_ising_matrix, ising_matrix_to_qubo_matrix


def assert_dict_equality(known_dict, check_dict):
    for key, value in known_dict.items():
        if isinstance(value, dict):
            # 如果值是字典，则递归调用 assert_dict_equality
            assert_dict_equality(value, check_dict[key])
        elif isinstance(value, np.ndarray):
            # 如果值是 NumPy 数组，则使用 np.array_equal() 进行比较
            assert np.array_equal(value, check_dict[key]), f"字典中的矩阵 {key} 内容不相等"
        else:
            # 对其他类型的数据进行简单相等性检查
            assert value == check_dict[key], f"字典中的 {key} 数据不相等"


def test_ising_to_qubo():
    ising_mat = np.array([[0, 1, -11, 20, 3],
                          [0, 0, 2, -1, -4],
                          [0, 0, 0, 2, 5],
                          [0, 0, 0, 0, 4],
                          [0, 0, 0, 0, 0]])
    qubo_mat, bias = ising_matrix_to_qubo_matrix(ising_mat, False)
    vec_x = np.array([0, 1, 0, 1, 1])
    vec_y = vec_x * 2 - 1
    hmt1 = vec_x.dot(qubo_mat).dot(vec_x) + bias
    hmt2 = - vec_y.dot(ising_mat).dot(vec_y)
    assert hmt1 == hmt2
    assert (np.triu(qubo_mat) == qubo_mat).all()


def test_qubo_to_ising():
    qubo_mat = np.array([[-14, 4, -44, 80],
                         [-0, -12, 8, -4],
                         [-0, -0, 24, 8],
                         [-0, -0, -0, -34]])
    ising_mat, bias = qubo_matrix_to_ising_matrix(qubo_mat)
    vec_x = np.array([0, 1, 1, 1])
    vec_y = vec_x * 2 - 1
    vec_y = np.append(vec_y, np.array([1]))
    hmt1 = vec_x.dot(qubo_mat).dot(vec_x)
    hmt2 = - vec_y.dot(ising_mat).dot(vec_y) + bias
    assert hmt1 == hmt2
    assert (ising_mat.T == ising_mat).all()


def test_cim_ising_model():
    b1, b2 = kw.core.Binary("b1"), kw.core.Binary("b2")
    q = b1 + b2 + 2 * b1 * b2
    qubo_model = kw.qubo.QuboModel(q)
    ci = kw.conversion.qubo_model_to_ising_model(qubo_model)

    _qubo_model = kw.qubo.QuboModel(q)
    _qubo_matrix = _qubo_model.get_matrix()
    _ising_matrix, _bias = kw.conversion.qubo_matrix_to_ising_matrix(_qubo_matrix)
    _ci = {'cim_ising_matrix': _ising_matrix, 'bias': _bias, 'variables': {'bb1': 0, 'bb2': 1, 'a__spin__': 2},
           'qubo_matrix': _qubo_matrix}
    assert_dict_equality(ci, _ci)


def test_qubo_model_to_qubo_matrix():
    b1, b2 = kw.core.Binary("b1"), kw.core.Binary("b2")
    q = b1 + b2 + 2 * b1 * b2
    qubo_model = kw.qubo.QuboModel(q)
    q_matrix = qubo_model.get_matrix()
    assert ((q_matrix == np.array([[1, 2], [0, 1]])).all()), "qubo matrix does not match"

    variables = qubo_model.get_variables()
    assert (variables == {'bb1': 0, 'bb2': 1}), "variables do not match"

    offset = qubo_model.get_offset()
    assert offset == 0, "offset does not match"


def test_qubo_matrix_to_qubo_model():
    q_mat = np.array([[0, 1, -11],
                      [0, 0, 2],
                      [0, 0, 0]])
    q_model = qubo_matrix_to_qubo_model(q_mat)
    ans = {('bb[1]', 'bb[2]'): 2, ('bb[0]', 'bb[2]'): -11, ('bb[0]', 'bb[1]'): 1}
    assert q_model.objective.coefficient == ans

    q_mat = np.random.randn(12, 12)
    q_mat = np.triu(q_mat)
    q_model = qubo_matrix_to_qubo_model(q_mat)
    q_mat2 = q_model.get_matrix()
    print(q_mat, q_mat2)
    assert (q_mat2 == q_mat).all()


mat = np.array([[-0., -0.125, -0., -1.125],
                [-0.125, -0., -0., -0.375],
                [-0., -0., -0., -0.5],
                [-1.125, -0.375, -0.5, -0.]])


def test_make():
    b1, b2, b3 = kw.core.Binary("b1"), kw.core.Binary("b2"), kw.core.Binary("b3")
    q = b1 * b2 + b1 * b1 + 3 * b1 + b2 * b2 + 2 * b3
    qubo_model = kw.qubo.QuboModel(q)
    ising_model = kw.conversion.qubo_model_to_ising_model(qubo_model)
    assert (ising_model.matrix == mat).all(), "自动make出现问题"


def test_make_no_constraint():
    b1, b2, b3 = kw.core.Binary("b1"), kw.core.Binary("b2"), kw.core.Binary("b3")
    q = b1 * b2 + b1 * b1 + 3 * b1 + b2 * b2 + 2 * b3
    qubo_model = kw.qubo.QuboModel(q)
    ising_model = kw.conversion.qubo_model_to_ising_model(qubo_model)
    assert (ising_model.matrix == mat).all(), "自动make出现问题"
