"""
Solves the Traveling Salesman Problem (TSP) using a QUBO formulation.
The distance matrix is used to construct a QUBO model with constraints ensuring a valid Hamiltonian cycle.
The model is solved using a brute-force optimizer from the kaiwu library.
"""

import numpy as np
import kaiwu as kw


def is_edge_used(x: np.ndarray, u: int, v: int) :
    """
    Determine whether the edge (u, v) is used in the path.

    Args:
        x (ndarray): Decision variable matrix.

        u (int): Start node.

        v (int): End node.

    Returns:
        ndarray: Decision variable corresponding to the edge (u, v).
    """
    return kw.core.quicksum([x[u, j] * x[v, j + 1] for j in range(-1, x.shape[0] - 1)])


if __name__ == '__main__':

    # Import distance matrix
    distance_matrix = np.array([[0, 13, 11, 16, 8],
                                [13, 0, 7, 14, 9],
                                [11, 7, 0, 10, 9],
                                [16, 14, 10, 0, 12],
                                [8, 9, 9, 12, 0]])

    # Get the number of nodes
    # pylint: disable=duplicate-code
    n = distance_matrix.shape[0]

    # Create qubo variable matrix
    path_matrix = kw.core.ndarray((n, n), "x", kw.core.Binary)

    # Get sets of edge and non-edge pairs
    edges = [(u, v) for u in range(n) for v in range(n) if distance_matrix[u, v] != 0]
    no_edges = [(u, v) for u in range(n) for v in range(n) if distance_matrix[u, v] == 0]

    qubo_model = kw.qubo.QuboModel()
    # TSP path cost
    qubo_model.set_objective(kw.core.quicksum([distance_matrix[u, v] * is_edge_used(path_matrix, u, v) for u, v in edges]))

    # Node constraint: Each node must belong to exactly one position
    qubo_model.add_constraint((path_matrix.sum(axis=0) - 1) ** 2 == 0, "sequence_cons", penalty=20)

    # Position constraint: Each position can have only one node
    qubo_model.add_constraint((path_matrix.sum(axis=1) - 1) ** 2 == 0, "node_cons", penalty=20)

    # Edge constraint: Pairs without edges cannot appear in the path
    qubo_model.add_constraint(kw.core.quicksum([is_edge_used(path_matrix, u, v) for u, v in no_edges]) == 0,
                              "connect_cons", penalty=20)

    # Perform calculation using SA optimizer
    solver = kw.solver.SimpleSolver(kw.classical.BruteForceOptimizer())

    sol_dict, qubo_val = solver.solve_qubo(qubo_model)
    print(sol_dict)

    # Check the hard constraints for validity and path length
    unsatisfied_count, res_dict = qubo_model.verify_constraint(sol_dict)
    print("unsatisfied constraint: ", unsatisfied_count)
    print("value of constraint term", res_dict)

    # Calculate the path length using path_cost
    path_val = kw.core.get_val(qubo_model.objective, sol_dict)
    print(f'path_cost: {path_val}')

    if unsatisfied_count == 0:
        print('valid path')

        # Get the numerical value matrix of x
        x_val = kw.core.get_array_val(path_matrix, sol_dict)
        # Find the indices of non-zero items
        nonzero_index = np.array(np.nonzero(x_val.T))[1]
        # Print the path order
        print(nonzero_index)
    else:
        print('invalid path')

