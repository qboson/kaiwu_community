# Kaiwu SDK 社区版

<img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version"> <img src="https://img.shields.io/badge/License-Apache%202.0-green" alt="License">

**语言版本**: [中文](https://github.com/qboson/kaiwu_community/blob/main/README_ZH.md) | [English](https://github.com/qboson/kaiwu_community/blob/main/README.md)

---

[Kaiwu SDK 社区版](https://kaiwu.qboson.com) 是一款专为 QUBO(二次无约束二进制优化)问题设计的 Python 开发工具包,提供快速建模、灵活扩展和高效求解能力。

## 安装

从源码安装:

```bash
git clone <repository-url>
cd kaiwu_community
pip install -e .
```

**环境要求:**
* Python 3.10.x (仅支持 Python 3.10 系列版本，暂不支持 3.11+)
* Make(用于开发构建)
* Virtualenv(可选,用于环境隔离)

更多安装信息,请参阅 [安装文档](https://kaiwu-community.readthedocs.io/zh-cn/latest/source/getting_started/sdk_installation_instructions.html)。

---

## 快速开始

### 学习资源

* [Kaiwu SDK 帮助中心](https://kaiwu-community.readthedocs.io/zh-cn/latest/index.html) - 查看详细文档，学习 QUBO 建模和求解
* [示例代码](https://github.com/qboson/kaiwu_community/blob/main/example/) - 查看完整代码示例

### 获取帮助

* [开发者社区](https://kaiwu.qboson.com/portal.php) - 参与社区活动并与其他开发者交流
* [GitHub Issues](https://github.com/qboson/kaiwu_community/issues) - 提交问题或功能请求


### 示例: 旅行商问题 (TSP)

示例代码将展示如何使用 Kaiwu SDK 社区版求解旅行商问题，包含以下步骤:

* 使用距离矩阵构建 TSP 问题模型
* 定义 QUBO 目标函数和约束条件
* 使用内置求解器求解模型
* 验证求解结果的有效性

完整的 TSP 示例代码请查看 [example/tsp_sdk_1_2_doc_example.py](https://github.com/qboson/kaiwu_community/blob/main/example/tsp_sdk_1_2_doc_example.py)。

更多详细说明请参考 [TSP 帮助文档](https://kaiwu-community.readthedocs.io/zh-cn/latest/source/getting_started/tsp.html)。

---

## 应用场景

Kaiwu SDK 适用于:

* **组合优化**: 旅行商问题(TSP)、背包问题、图着色、最大割
* **机器学习**: 特征选择、聚类分析、模型压缩
* **量子计算研究**: QUBO 模型研究、求解器开发、量子算法验证

---

## 贡献

欢迎社区贡献! 🎉

你可以扩展 SDK 功能,例如新的求解器实现、经典优化算法、示例程序和文档。

### 贡献示例

通过继承基类快速扩展功能:

```python
from kaiwu.optimizer import OptimizerBase

class NewOptimizer(OptimizerBase):
    def optimize(self, model):
        # 自定义优化逻辑
        pass

# 使用自定义优化器
solver = kaiwu.solver.SimpleSolver(NewOptimizer())
```

➡️ 详细贡献指南请参考 [Contributing Guide](https://github.com/qboson/kaiwu_community/blob/main/CONTRIBUTING.md)。

---

## 许可证

本项目基于 **Apache License 2.0** 许可证开源。详情请参见 [LICENSE](https://github.com/qboson/kaiwu_community/blob/main/LICENSE) 文件。