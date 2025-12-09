# -*- coding: utf-8 -*-
"""
模块: qubo

功能: QUBO还原变量值
"""
import numbers
import numpy as np

# 构造结果字典
# 输入：结果向量，从ci.get_variables()得到的字典
def get_sol_dict(solution, vars_dict):
    """根据解向量和变量字典生成结果字典.

    Args:
        solution (np.ndarray): 解向量（spin）。

        vars_dict (dict): 变量字典，用cim_ising_model.get_variables()生成。

    Returns:
        dict: 结果字典。键为变量名，值为对应的spin值。

    Examples:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> a = kw.core.Binary("a")
        >>> b = kw.core.Binary("b")
        >>> c = kw.core.Binary("c")
        >>> d = a + 2 * b + 4 * c
        >>> d = kw.qubo.QuboModel(d)
        >>> d_ising = kw.conversion.qubo_model_to_ising_model(d)
        >>> vars = d_ising.get_variables()
        >>> s = np.array([1, -1, 1])
        >>> kw.core.get_sol_dict(s, vars)
        {'a': np.float64(1.0), 'b': np.float64(0.0), 'c': np.float64(1.0)}
        """
    # 除了虚拟变量以外，遍历vars_dict字典，对每个键都找到其位置，并在bin_c中取值。
    return dict((k, (solution[vars_dict[k]] + 1) / 2)
                for k, _ in vars_dict.items() if k != '__spin__')


def get_val(qubo, sol_dict):
    """根据结果字典将spin值带入qubo变量.

    Args:
        qubo (QUBO表达式): QUBO表达式

        sol_dict (dict): 由get_sol_dict生成的结果字典。

    Returns:
        float: 带入qubo后所得的值

    Examples:
        >>> import kaiwu_community as kw
        >>> import numpy as np
        >>> a = kw.core.Binary("a")
        >>> b = kw.core.Binary("b")
        >>> c = kw.core.Binary("c")
        >>> d = a + 2 * b + 4 * c
        >>> qubo_model = kw.qubo.QuboModel(d)
        >>> d_ising = kw.conversion.qubo_model_to_ising_model(qubo_model)
        >>> ising_vars = d_ising.get_variables()
        >>> s = np.array([1, -1, 1])
        >>> sol_dict = kw.core.get_sol_dict(s, ising_vars)
        >>> kw.core.get_val(d, sol_dict)
        np.float64(5.0)
    """
    if isinstance(qubo, numbers.Number):
        return qubo
    value = qubo.offset  # 结果加上offset
    for k, val in qubo.coefficient.items():  # 遍历所有键值对
        for var in k:  # 对于每个键也遍历元组
            val *= sol_dict.get(var[1:], 0.0)
        value += val  # 累加一项的结果
    return value



def get_array_val(array, sol_dict):
    """根据结果字典将spin值带入qubo数组变量.

    Args:
        array (QUBOArray): QUBO数组

        sol_dict (dict): 由get_sol_dict生成的结果字典。

    Returns:
        np.ndarray: 带入qubo数组后所得的值数组

    Examples:
        >>> import kaiwu_community as kw
        >>> import numpy as np
        >>> x = kw.core.ndarray((2, 2), "x", kw.core.Binary)
        >>> y = x.sum()
        >>> y = kw.qubo.QuboModel(y)
        >>> y_ising = kw.conversion.qubo_model_to_ising_model(y)
        >>> ising_vars = y_ising.get_variables()
        >>> s = np.array([1, -1, 1, -1])
        >>> sol_dict = kw.core.get_sol_dict(s, ising_vars)
        >>> kw.core.get_array_val(x, sol_dict)
        array([[1., 0.],
               [1., 0.]])
    """
    val_array = np.zeros(array.shape)  # 创建与qubo数组相同形状的空数组
    for index in np.ndindex(array.shape):  # 遍历数组的所有下标
        val_array[index] = get_val(array[index], sol_dict)  # 每个下标都调用get_val
    return val_array


if __name__ == '__main__':
    import doctest
    doctest.testmod()
