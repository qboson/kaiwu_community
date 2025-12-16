# Kaiwu SDK Community Edition

<img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version"> <img src="https://img.shields.io/badge/License-Apache%202.0-green" alt="License">

**Language Versions**: [中文](README_ZH.md) | [English](README.md)

## 📖 Project Overview

The **Kaiwu SDK Community Edition** is a Python development toolkit designed specifically for **QUBO (Quadratic Unconstrained Binary Optimization)** problems. It provides underlying data structure implementations and a modeling framework, enabling developers to quickly build custom models and solvers for efficient QUBO problem modeling and solving.

### 🎯 Core Values

- **Rapid Modeling**: Provides a simple and easy-to-use API for quickly building complex QUBO models
- **Flexible Extension**: Modular design allows developers to easily extend new solvers and optimization algorithms
- **Built-in Tools**: Includes basic solvers and optimizers for quickly validating model effects
- **Open Source Freedom**: Based on Apache 2.0 license, fully open source, supporting commercial and non-commercial use

### 📋 Application Scenarios

Kaiwu SDK Community Edition is suitable for the following scenarios:
- Researchers exploring QUBO problem modeling and solving algorithms
- Developers building custom QUBO solvers and optimizers
- Students learning quantum computing and combinatorial optimization problems
- Enterprises developing QUBO-based solution prototypes

---

## 🚀 Prerequisites

Before using the SDK, make sure you have the following installed:

* **Python** ≥ 3.10
* **Make** (for running build/test commands)
* **Virtualenv** (optional, for isolated environments: `pip install virtualenv`)

---

## 🛠 Getting Started

Please refer to the [SDK Documentation](https://kaiwu-sdk-docs.qboson.com/en/) for detailed usage instructions.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd kaiwu_community
```

### 2. Set Up the Environment

Create a virtual environment and install dependencies. You can also run linting and tests with:

```bash
make all_tests
```

---

## 📘 Example Programs

### Traveling Salesman Problem (TSP) Example

The Traveling Salesman Problem is a classic problem in combinatorial optimization, aiming to find the shortest path that visits all cities and returns to the starting point.

Kaiwu SDK Community Edition provides a complete TSP solving example, demonstrating how to model and solve this problem using a QUBO model:

* **File Path**: [example/tsp\_sdk\_1\_2\_doc\_example.py](example/tsp_sdk_1_2_doc_example.py)
* **Example Content**:
  - Building a TSP problem model using a distance matrix
  - Defining QUBO objective function and constraints
  - Solving the model using built-in solver
  - Validating the effectiveness of the solution

This example demonstrates the core functionalities of Kaiwu SDK, including QUBO model construction, constraint addition, model solving, and result validation.

---

## 🤝 Support

* Join the [Kaiwu User Community](https://kaiwu.qboson.com/portal.php) to connect with other users
* Visit the [Kaiwu SDK Help Center](https://kaiwu-sdk-docs.qboson.com/en/) for tutorials & knowledge base
* Open issues or request features on the **SDK GitHub repo**

---

## 🔧 Contributing

We welcome contributions! 🎉

You can extend the SDK by adding:

* New solver implementations
* Classical optimization algorithms
* Model conversion tools
* Example programs and documentation

### Contribution Example

Creating a custom optimizer by extending `OptimizerBase`:

```python
class NewOptimizer(OptimizerBase):
    ...
```

Using it with a solver:

```python
solver = kaiwu.solver.SimpleSolver(NewOptimizer())
```

➡️ See the [Contributing Guide](CONTRIBUTING.md) for full guidelines.

---

## 📜 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.

---

## 🏗 SDK Architecture

Kaiwu SDK Community Edition adopts a modular design, including the following core modules:

* **QUBO Model**: Provides QUBO problem modeling functionality
* **Solver Framework**: Supports multiple solvers and optimizers
* **Classical Optimizers**: Includes basic classical solving algorithms
* **Core Data Structures**: Provides efficient mathematical operation support

Architecture Overview:

![Kaiwu SDK Architecture](SDD/architecture.png)
