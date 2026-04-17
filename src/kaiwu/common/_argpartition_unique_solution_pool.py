"""
求解器的解集
"""

import numpy as np

from ._util import hamiltonian


class ArgpartitionUniquePool:
    """解集。使用argpartition的线性期望复杂度k小值来进行维护"""

    def __init__(self, mat, size, size_limit):
        """
        初始化
        输入：
            mat: ising矩阵
            size: 矩阵维度
            size_limit: 保留解的个数
        """
        self.mat = mat
        self.size = size
        self.size_limit = size_limit
        self.threshold = float("inf")  # 当前解集中最差的解的哈密顿量，用于过滤输入的解
        self.candidate_solutions = np.array([]).reshape(0, size)  # 缓存
        self.opt = np.array([]).reshape(0, size)  # 解集
        self.hamilton = []

    def extend(self, solutions, final=False):
        """插入多个解"""
        if solutions.size == 0:
            return
        self.candidate_solutions = np.concatenate(
            (self.candidate_solutions, solutions), axis=0
        )
        if self.candidate_solutions.shape[0] > 0 and (
            final
            or len(self.candidate_solutions) + len(self.opt) >= 2 * self.size_limit
        ):
            ha_candidate = hamiltonian(self.mat, self.candidate_solutions)
            filter_index = ha_candidate < self.threshold
            ha_candidate = ha_candidate[filter_index]
            self.candidate_solutions = self.candidate_solutions[filter_index]
            self.hamilton = np.concatenate((self.hamilton, ha_candidate), axis=0)

            self.candidate_solutions = np.concatenate(
                (self.opt, self.candidate_solutions), axis=0
            )
            hamilton, unique_solution = zip(
                *set(zip(self.hamilton, map(tuple, self.candidate_solutions)))
            )
            unique_solution = np.array(unique_solution)
            self.hamilton = np.array(hamilton)
            num = min(self.size_limit, len(unique_solution))
            indices = np.argpartition(self.hamilton, num - 1)[:num]
            self.opt = unique_solution[indices]
            self.hamilton = self.hamilton[indices]
            self.candidate_solutions = np.array([]).reshape(0, self.size)
            self.threshold = (
                max(self.hamilton) if len(self.opt) == self.size_limit else float("inf")
            )

    def get_solutions(self):
        """获取解集"""
        self.extend(
            np.array([]).reshape(0, self.size), final=True
        )  # 把缓存的解加入计算
        return self.opt

    def clear(self):
        """清空解集"""
        self.threshold = float("inf")
        self.candidate_solutions = np.array([]).reshape(0, self.size)
        self.opt = np.array([]).reshape(0, self.size)
        self.hamilton = []

    def to_json_dict(self):
        """转化为json字典

        Returns:
            dict: json字典
        """
        json_dict = {}
        self_dict = self.__dict__

        for attr_name, attr_value in self_dict.items():
            if isinstance(attr_value, np.ndarray):
                json_dict[attr_name] = attr_value.tolist()
            else:
                json_dict[attr_name] = attr_value
        return json_dict

    @classmethod
    def from_json_dict(cls, json_dict):
        """从json文件读取的dict构造HeapUniquePool对象

        Args:
            json_dict (dict): json字典

        Returns:
            ArgpartitionUniquePool: 对象实例
        """
        param_dict = json_dict.copy()
        param_dict["mat"] = np.array(json_dict["mat"])
        param_dict["candidate_solutions"] = np.array(json_dict["candidate_solutions"])
        param_dict["opt"] = np.array(json_dict["opt"])
        obj = cls(None, 0, 0)
        for attr_name, attr_value in param_dict.items():
            setattr(obj, attr_name, attr_value)
        return obj
