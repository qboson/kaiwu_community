# Kaiwu Community

<img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version"> <img src="https://img.shields.io/badge/License-Apache%202.0-green" alt="License">

**Language**: [中文](https://github.com/qboson/kaiwu_community/blob/main/README_ZH.md) | [English](https://github.com/qboson/kaiwu_community/blob/main/README.md)

---

Kaiwu Community is a Python development toolkit designed specifically for QUBO (Quadratic Unconstrained Binary Optimization) problems, providing rapid modeling, flexible extension, and efficient solving capabilities.

## Installation

```bash
pip install kaiwu_community
```

**Requirements:**
* Python 3.10.x
* Make (for development builds)
* Virtualenv (optional, for environment isolation)

For more installation information, please refer to the [Installation Documentation](https://kaiwu-community.readthedocs.io/zh-cn/latest/source/getting_started/sdk_installation_instructions.html).

---

## Quick Start

### Learning Resources

* [Kaiwu SDK Help Center](https://kaiwu-community.readthedocs.io/zh-cn/latest/index.html) - View detailed documentation and learn QUBO modeling and solving
* [Example Code](https://github.com/qboson/kaiwu_community/blob/main/example/) - Browse complete code examples

### Getting Help

* [Developer Community](https://kaiwu.qboson.com/portal.php) - Participate in community activities and connect with other developers
* [GitHub Issues](https://github.com/qboson/kaiwu_community/issues) - Submit issues or feature requests


### Example: Traveling Salesman Problem (TSP)

This example demonstrates how to solve the Traveling Salesman Problem using Kaiwu SDK Community, including the following steps:

* Build a TSP problem model using a distance matrix
* Define QUBO objective function and constraints
* Solve the model using built-in solvers
* Validate the solution results

For the complete TSP example code, please see [example/tsp_sdk_1_2_doc_example.py](https://github.com/qboson/kaiwu_community/blob/main/example/tsp_sdk_1_2_doc_example.py).

For more detailed explanations, please refer to the [TSP Documentation](https://kaiwu-community.readthedocs.io/zh-cn/latest/source/getting_started/tsp.html).

---

## Application Scenarios

Kaiwu SDK is suitable for:

* **Combinatorial Optimization**: Traveling Salesman Problem (TSP), Knapsack Problem, Graph Coloring, Max-Cut
* **Machine Learning**: Feature Selection, Cluster Analysis, Model Compression
* **Quantum Computing Research**: QUBO Model Research, Solver Development, Quantum Algorithm Verification

---

## Contributing

Community contributions are welcome! 🎉

You can extend SDK functionality, such as new solver implementations, classical optimization algorithms, example programs, and documentation.

### Contribution Example

Quickly extend functionality by inheriting base classes:

```python
from kaiwu_community.core import OptimizerBase, SolverBase
import kaiwu_community

# Custom optimizer
class CustomOptimizer(OptimizerBase):
    def solve(self, ising_matrix=None):
        # Implement custom optimization logic
        pass

# Custom solver
class CustomSolver(SolverBase):
    def solve_qubo(self, model):
        # Implement custom solver logic
        self._optimizer.solve()
        pass

# Modeling
qubo_model = kaiwu_community.qubo.QuboModel()
# Calling the custom component
optimizer = CustomOptimizer()
solver = CustomSolver(optimizer)
result = solver.solve_qubo(qubo_model)
```

➡️ For detailed contribution guidelines, please refer to the [Contributing Guide](https://github.com/qboson/kaiwu_community/blob/main/CONTRIBUTING.md).

---

## License

This project is open-sourced under the **Apache License 2.0**. For details, please see the [LICENSE](https://github.com/qboson/kaiwu_community/blob/main/LICENSE) file.