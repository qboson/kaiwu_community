"""
Tests for core._matrix module
"""
import os
import sys
import numpy as np
import pytest
from numpy.testing import assert_array_equal, assert_array_almost_equal

from common.config import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

import kaiwu_community as kw
from kaiwu_community.core._matrix import BinaryExpressionNDArray, dot, ndarray
from kaiwu_community.core import Binary, Expression


def test_dot_basic():
    """Test basic matrix dot product"""
    mat1 = np.array([[1, 2], [3, 4]])
    mat2 = np.array([[5, 6], [7, 8]])
    result = dot(mat1, mat2)
    expected = np.array([[19, 22], [43, 50]])
    assert_array_equal(result, expected)


def test_dot_vector():
    """Test dot product with vectors"""
    vec1 = np.array([1, 2, 3])
    vec2 = np.array([4, 5, 6])
    result = dot(vec1, vec2)
    assert result == 32  # 1*4 + 2*5 + 3*6


def test_dot_matrix_vector():
    """Test dot product between matrix and vector"""
    mat = np.array([[1, 2], [3, 4]])
    vec = np.array([5, 6])
    result = dot(mat, vec)
    expected = np.array([17, 39])
    assert_array_equal(result, expected)


def test_dot_invalid_input():
    """Test dot product with invalid inputs"""
    mat1 = np.array([[1, 2], [3, 4]])
    mat2 = np.array([[5, 6, 7], [8, 9, 10], [11, 12, 13]])

    with pytest.raises(ValueError):
        dot([1, 2], [3, 4])  # Not numpy arrays

    with pytest.raises(ValueError):
        dot(mat1, mat2)  # Incompatible dimensions


def test_binary_expression_array_creation():
    """Test BinaryExpressionArray creation"""
    shape = (2, 3)
    arr = BinaryExpressionNDArray(shape, dtype=Expression)
    assert arr.shape == shape
    assert arr.dtype == Expression


def test_binary_expression_array_comparison():
    """Test BinaryExpressionArray comparison operations"""
    x = kw.core.Binary('x')
    y = kw.core.Binary('y')
    arr1 = BinaryExpressionNDArray((2,), dtype=Expression)
    arr2 = BinaryExpressionNDArray((2,), dtype=Expression)
    arr1[0], arr1[1] = x, y
    arr2[0], arr2[1] = y, x

    # Test all comparison operators
    assert str(arr1 < arr2) == '[-y+x<0, -x+y<0,]'
    assert str(arr1 <= arr2) == '[-y+x<=0, -x+y<=0,]'
    assert str(arr1 > arr2) == '[-y+x>0, -x+y>0,]'
    assert str(arr1 >= arr2) == '[-y+x>=0, -x+y>=0,]'
    assert str(arr1 == arr2) == '[-y+x==0, -x+y==0,]'


def test_binary_expression_array_dot():
    """Test BinaryExpressionArray dot product"""
    x = kw.core.Binary('x')
    y = kw.core.Binary('y')
    arr1 = BinaryExpressionNDArray((2,), dtype=Expression)
    arr2 = BinaryExpressionNDArray((2,), dtype=Expression)
    arr1[0], arr1[1] = x, y
    arr2[0], arr2[1] = y, x

    result = arr1.dot(arr2)
    assert isinstance(result, Expression)


def test_binary_expression_array_sum():
    """Test BinaryExpressionArray sum operation"""
    x = kw.core.Binary('x')
    y = kw.core.Binary('y')
    arr = BinaryExpressionNDArray((2, 2), dtype=Expression)
    arr[0, 0], arr[0, 1], arr[1, 0], arr[1, 1] = x, y, x, y

    # Test sum without axis
    total_sum = arr.sum()
    assert isinstance(total_sum, Expression)

    # Test sum along axis
    row_sum = arr.sum(axis=0)
    assert isinstance(row_sum, BinaryExpressionNDArray)
    assert row_sum.shape == (2,)


def test_binary_expression_array_sum_with_out():
    """Test BinaryExpressionArray sum with out parameter"""
    x = kw.core.Binary('x')
    y = kw.core.Binary('y')
    arr = BinaryExpressionNDArray((2, 2), dtype=Expression)
    arr[0, 0], arr[0, 1], arr[1, 0], arr[1, 1] = x, y, x, y

    out = BinaryExpressionNDArray((2,), dtype=Expression)
    result = arr.sum(axis=0, out=out)
    assert result is out
    assert result.shape == (2,)


def test_ndarray_creation():
    """Test ndarray creation with different shapes and functions"""
    # Test with 1D shape
    arr1 = ndarray(3, "x", Binary)
    assert arr1.shape == (3,)
    assert all(isinstance(x, Expression) for x in arr1)

    # Test with 2D shape
    arr2 = ndarray((2, 2), "y", Binary)
    assert arr2.shape == (2, 2)
    assert all(isinstance(x, Expression) for x in arr2.flatten())

    # Test with list shape
    arr3 = ndarray([2, 3], "z", Binary)
    assert arr3.shape == (2, 3)
    assert all(isinstance(x, Expression) for x in arr3.flatten())


def test_ndarray_with_parameters():
    """Test ndarray creation with additional parameters"""

    def custom_var(name, param1=None):
        return Binary(f"{name}_{param1}")

    arr = ndarray(2, "x", custom_var, var_func_param=("param1",))
    assert arr.shape == (2,)
    assert all(isinstance(x, Expression) for x in arr)


def test_binary_expression_array_matmul():
    """Test BinaryExpressionArray matrix multiplication operator @"""
    x = kw.core.Binary('x')
    y = kw.core.Binary('y')
    arr1 = BinaryExpressionNDArray((2,), dtype=Expression)
    arr2 = BinaryExpressionNDArray((2,), dtype=Expression)
    arr1[0], arr1[1] = x, y
    arr2[0], arr2[1] = y, x

    result = arr1 @ arr2
    assert isinstance(result, Expression)


def test_binary_expression_array_invalid_sum():
    """Test BinaryExpressionArray sum with invalid input"""
    with pytest.raises(ValueError):
        BinaryExpressionNDArray.sum(None)  # Not a numpy array
