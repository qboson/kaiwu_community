# -*- coding: utf-8 -*-
"""
SDK 公用模块
"""
import numpy as np


class JsonSerializableMixin:
    """
    序列化器

    """

    def to_json_dict(self, exclude_fields=("_optimizer",)):
        """转化为json字典

        Returns:
            dict: json字典
        """
        object_dict = self.__dict__
        json_dict = {}

        for attr_name, attr_value in object_dict.items():
            if attr_name in exclude_fields:
                continue
            attr_type = attr_name + "$type"
            if isinstance(attr_value, np.ndarray):
                json_dict[attr_name] = attr_value.tolist()
                json_dict[attr_type] = "np.ndarray"
            elif isinstance(attr_value, list):
                json_dict[attr_type] = "list"

                json_dict[attr_name] = [
                    item.to_json_dict() if hasattr(item, "to_json_dict") else item
                    for item in attr_value
                ]

            elif hasattr(attr_value, "to_json_dict"):
                data = attr_value.to_json_dict()
                json_dict[attr_name] = data
                json_dict[attr_type] = "JsonSerializableMixin"
            elif isinstance(attr_value, np.number):
                json_dict[attr_name] = float(attr_value)
            elif attr_name == "sub_indices" and attr_value is not None:
                json_dict[attr_name] = np.array(attr_value).tolist()
            elif attr_name == "rng":
                state = self.rng.__getstate__()
                json_dict[attr_name] = state
            else:
                json_dict[attr_name] = attr_value
        return json_dict

    def load_json_dict(self, json_dict):
        """从json文件读取的dict恢复对象

        Returns:
            dict: json字典
        """
        # Nothing stored before, just return
        if json_dict is None:
            return

        param_dict = json_dict.copy()

        for attr_name, attr_value in param_dict.items():
            if "$type" in attr_name:
                continue
            attr_type = json_dict.get(attr_name + "$type")
            if isinstance(attr_value, dict) and attr_type == "JsonSerializableMixin":
                instance = getattr(self, attr_name)
                instance.load_json_dict(attr_value)
                continue
            if attr_type == "np.ndarray":
                attr_value = np.array(attr_value)
            elif attr_name == "rng":
                rng_obj = np.random.default_rng()
                rng_obj.__setstate__(attr_value)
                attr_value = rng_obj
            setattr(self, attr_name, attr_value)
