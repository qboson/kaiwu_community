"""
Tests for common._util module
"""

import os
import sys
import numpy as np
from numpy.testing import assert_equal, assert_allclose

from common.config import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR, "src"))
from kaiwu.common import hamiltonian, check_symmetric


def test_hamiltonian_simple():
    """Test hamiltonian calculation with simple matrix"""
    ising_matrix = np.array([[0, 1], [1, 0]])
    c_list = np.array([[1, -1], [-1, 1]])
    result = hamiltonian(ising_matrix, c_list)
    expected = np.array([2, 2])
    assert_allclose(result, expected)


def test_hamiltonian_larger():
    """Test hamiltonian calculation with larger matrix"""
    ising_matrix = np.array([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
    c_list = np.array([[1, -1, 1], [-1, 1, -1], [1, -1, 1]])
    result = hamiltonian(ising_matrix, c_list)
    # Expected values calculated manually
    expected = np.array([4, 4, 4])
    assert_allclose(result, expected)


def test_check_symmetric_true():
    """Test check_symmetric with symmetric matrix"""
    matrix = np.array([[1, 2, 3], [2, 4, 5], [3, 5, 6]])
    assert check_symmetric(matrix)


def test_check_symmetric_false():
    """Test check_symmetric with non-symmetric matrix"""
    matrix = np.array([[1, 2, 3], [2, 4, 5], [3, 6, 6]])  # Note: 6 != 5
    assert check_symmetric(matrix) == False


def test_check_symmetric_almost():
    """Test check_symmetric with almost symmetric matrix (within tolerance)"""
    matrix = np.array([[1, 2, 3], [2, 4, 5], [3, 5 + 1e-9, 6]])
    assert check_symmetric(matrix)


def test_check_symmetric_custom_tolerance():
    """Test check_symmetric with custom tolerance"""
    matrix = np.array([[1, 2, 3], [2, 4, 5], [3, 5 + 1e-5, 6]])
    assert check_symmetric(matrix, tolerance=1e-4) == True
    assert check_symmetric(matrix, tolerance=1e-6) == False
