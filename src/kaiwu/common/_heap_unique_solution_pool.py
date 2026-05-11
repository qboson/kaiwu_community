"""
求解器的解集
"""

import copy
import heapq
import numpy as np

from kaiwu.common._json_serializable_mixin import JsonSerializableMixin
from kaiwu.common._util import hamiltonian


class HeapUniquePool(JsonSerializableMixin):
    """解集。使用堆来进行维护"""

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
        self.minheap_opt = []  # 保留解集的堆
        self.opt_set = set()  # 用于去重

    def extend(self, solutions):
        """插入多个解"""
        hamilton = hamiltonian(self.mat, solutions)
        for j in range(hamilton.shape[0]):
            self.push(solutions[j], hamilton[j])

    def push(self, solution, hamilton):
        """添加一个解"""
        solution_tuple = tuple(solution)
        if (
            len(self.minheap_opt) < self.size_limit
            or -self.minheap_opt[0][0] > hamilton
        ) and solution_tuple not in self.opt_set:
            heapq.heappush(self.minheap_opt, (-hamilton, solution_tuple))
            self.opt_set.add(solution_tuple)
            if len(self.minheap_opt) > self.size_limit:
                solution_vec = heapq.heappop(self.minheap_opt)[1]
                self.opt_set.remove(solution_vec)

    def get_solutions(self):
        """返回维护的解，个数为self.size_limit"""
        c_set = np.array([x[1] for x in self.minheap_opt])
        hamilton = hamiltonian(self.mat, c_set)
        index = np.argsort(hamilton)
        c_sorted = c_set[index]
        c_sorted[c_sorted[:, -1] <= 0, :] *= -1
        return c_sorted

    def clear(self):
        """清空解集"""
        self.minheap_opt = []
        self.opt_set = set()

    def to_json_dict(self, exclude_fields=None):
        """转化为json字典

        Returns:
            dict: json字典
        """
        json_dict = super().to_json_dict(exclude_fields=("minheap_opt", "opt_set"))
        heap_opt_list = []
        for hmt, sol in self.minheap_opt:
            heap_opt_list.append([float(hmt), list(sol)])
        json_dict["minheap_opt"] = heap_opt_list
        return json_dict

    def load_json_dict(self, json_dict):
        """从json文件读取的dict构造HeapUniquePool对象

        Args:
            json_dict (dict): json字典

        Returns:
            HeapUniquePool: 对象实例
        """
        super().load_json_dict(json_dict)
        minheap_opt = copy.deepcopy(json_dict["minheap_opt"])
        for item in minheap_opt:
            item[1] = tuple(item[1])
            self.opt_set.add(item[1])
        self.minheap_opt = minheap_opt
