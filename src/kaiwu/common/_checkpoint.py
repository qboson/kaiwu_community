# -*- coding: utf-8 -*-
"""
管理 checkpoint 保存的路径和各个对象 checkpoint 的命名。

该模块提供了一个 `CheckpointManager` 类，用于管理 checkpoint 的保存路径和命名规则。
通过设置 `CheckpointManager.save_dir`，可以指定 checkpoint 的保存目录。
"""
import os
import json
import logging

logger = logging.getLogger(__name__)


class CheckpointManager:
    """
    管理 checkpoint, 保存对象的运行状态，用于后续断点处恢复运行
    通过设置 `CheckpointManager.save_dir`，可以指定 checkpoint 的保存目录。

    Args:
        save_dir (str): checkpoint 的保存目录。

    """

    save_dir = None
    _class_name_counter = {}  # 用于更新生成name的id
    _dict_obj_identity = {}  # used to record the mapping of obj and savename

    @classmethod
    def _clear(cls):
        """刷新状态"""
        cls._class_name_counter = {}
        _dict_obj_file_name = {}

    @classmethod
    def _get_identity(cls, obj):
        """获取用于保存checkpoint的名字，名字基于类名生成

        Args:
            obj (Object): 要保存的对象

        Returns:
            str: 用于保存checkpoint的名字
        """
        if cls._dict_obj_identity.get(obj) is not None:
            return cls._dict_obj_identity.get(obj)

        class_name = obj.__class__.__name__
        if class_name in cls._class_name_counter:
            cls._class_name_counter[class_name] += 1
        else:
            cls._class_name_counter[class_name] = 1

        cls._dict_obj_identity[obj] = (
            f"{class_name}_{str(cls._class_name_counter[class_name])}"
        )

        return cls._dict_obj_identity.get(obj)

    @classmethod
    def get_path(cls, obj):
        """获取对象checkpoint的路径

        Args:
            obj (Object): 保存的对象

        Returns:
            str: checkpoint路径
        """

        identity = CheckpointManager._get_identity(obj)
        return os.path.join(CheckpointManager.save_dir, identity + "_checkpoint.json")

    @classmethod
    def load(cls, obj):
        """加载串行化的对象

        Args:
            obj (Object): 保存的对象

        Returns:
            str: json dict形式的对象
        """

        if CheckpointManager.save_dir is None:
            return None
        json_dict = None
        if os.path.exists(CheckpointManager.get_path(obj)):
            with open(
                CheckpointManager.get_path(obj), "r", encoding="utf8"
            ) as load_file:
                json_dict = json.load(load_file)
                logger.info(
                    "The previous state loaded in %s. clear the folder %s if it is not your will.",
                    CheckpointManager.save_dir,
                    CheckpointManager.save_dir,
                )
        return json_dict

    @classmethod
    def dump(cls, obj):
        """对象串行化后存储在磁盘上

        Args:
            obj (Object): 保存的对象

        Returns:
            None
        """
        if CheckpointManager.save_dir is None:
            return

        with open(CheckpointManager.get_path(obj), "w", encoding="utf8") as save_file:
            json.dump(obj.to_json_dict(), save_file)
