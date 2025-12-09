"""
模块: qubo

功能: 提供QUBOModel相关的功能
"""
import logging
import numpy as np
from kaiwu_community.core import BinaryModel, ndarray, Binary, quicksum
from kaiwu_community.qubo._repr import _qubo_check, _qubo_details

logger = logging.getLogger(__name__)


class QuboModel(BinaryModel):
    """支持添加约束的QUBO模型类

    Args:
        objective (QuboExpression, optional): 目标函数. 默认为None
    """

    def __init__(self, objective=None):
        super().__init__(objective)
        self.qubo_expr_made = None

        self.made = False
        self.variables = None
        self.matrix = None

    def __repr__(self):
        return f"{self.__class__.__name__}({vars(self)!r})"

    def __str__(self):
        print_data = _qubo_details(self.objective)
        return print_data

    def invalidate_made_state(self):
        """Invalidate the made state when the model changes"""
        self.made = False
        self.qubo_expr_made = None
        self.matrix = None

    def make(self):
        """返回合并后的QUBO表达式

        Returns:
            BinaryExpression: 合并的约束表达式
        """
        if self.made:
            return self.qubo_expr_made

        constraint_list = self.get_constraints_expr_list()

        self.qubo_expr_made = self.objective + quicksum(constraint_list)

        variables_set = self.qubo_expr_made.get_variables()
        _qubo_check(variables_set, self.qubo_expr_made.coefficient)

        self.variables = dict(zip(variables_set, range(len(variables_set))))

        self.matrix = np.zeros((len(variables_set), len(variables_set)))
        for key in self.qubo_expr_made.coefficient:
            if len(key) == 2:
                self.matrix[self.variables[key[0]], self.variables[key[1]]] = \
                    self.qubo_expr_made.coefficient[key]
            else:
                self.matrix[self.variables[key[0]], self.variables[key[0]]] = \
                    self.qubo_expr_made.coefficient[key]
        self.made = True
        return self.qubo_expr_made

    def get_matrix(self):
        """获取QUBO矩阵

        Returns:
            numpy.ndarray: QUBO矩阵

        """
        self.compile_constraints()
        self.make()
        return self.matrix

    def get_variables(self):
        """获取qubo模型的variables"""
        self.compile_constraints()
        self.make()
        return self.variables

    def get_offset(self):
        """获取qubo模型的offset"""
        return self.objective.offset

    def get_sol_dict(self, qubo_solution):
        """根据解向量生成结果字典."""
        self.compile_constraints()
        self.make()
        return dict((k[1:], 1 if qubo_solution[idx] > 0 else 0)
                    for k, idx in self.variables.items() if k != '__spin__')


def calculate_qubo_value(qubo_matrix, offset, binary_configuration):
    """Q值计算器.

    Args:
        qubo_matrix (np.ndarray): QUBO矩阵.

        offset (float): 常数项

        binary_configuration (np.ndarray): 二进制配置

    Returns:
        output (float): Q值.

    Examples:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> matrix = np.array([[1., 0., 0.],
        ...                    [0., 1., 0.],
        ...                    [0., 0., 1.]])
        >>> offset = 1.8
        >>> binary_configuration = np.array([0, 1, 0])
        >>> qubo_value = kw.qubo.calculate_qubo_value(matrix, offset, binary_configuration)
        >>> print(qubo_value)
        2.8
    """
    return (binary_configuration.dot(qubo_matrix)).dot(binary_configuration) + offset


def qubo_matrix_to_qubo_model(qubo_mat):
    """将qubo矩阵转化为qubo模型

    Args:
        qubo_mat (np.ndarray): QUBO矩阵

    Returns:
        QuboModel: QUBO模型

    Examples:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> matrix = -np.array([[0, 8],
        ...                     [0, 0]])
        >>> kw.qubo.qubo_matrix_to_qubo_model(matrix).objective
        -8*b[0]*b[1]
    """
    vars_b = ndarray(len(qubo_mat), 'b', Binary)
    return QuboModel(vars_b.dot(qubo_mat).dot(vars_b))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
