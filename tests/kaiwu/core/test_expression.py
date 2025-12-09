"""
Tests for core._expression module
"""
import os
import sys
import pytest

from common.config import BASE_DIR

# Set the correct path for Kaiwu imports
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

from kaiwu_community.core._error import KaiwuError
from kaiwu_community.core._constraint import ConstraintDefinition
from kaiwu_community.core._expression import Expression, is_zero, update_constraint, _check_unit
from kaiwu_community.core import Binary


@pytest.fixture
def expr_x():
    return Binary('x')


@pytest.fixture
def expr_y():
    return Binary('y')


def test_is_zero():
    """Test the is_zero utility function."""
    assert is_zero(0)
    assert not is_zero(1)
    assert is_zero(Expression())
    assert not is_zero(Expression(offset=1))
    assert not is_zero(Expression({('bx',): 1}))


def test_update_constraint():
    """Test the update_constraint utility function."""
    origin = Expression()
    origin['hard_constraint'] = {'c1': 'info1'}
    result = Expression()

    update_constraint(origin, result)
    assert result['hard_constraint'] == {'c1': 'info1'}

    # Test merging
    result['hard_constraint'] = {'c2': 'info2'}
    update_constraint(origin, result)
    assert result['hard_constraint'] == {'c1': 'info1', 'c2': 'info2'}


def test_check_unit():
    """Test the _check_unit string formatting helper."""
    assert _check_unit("1*x") == "x"
    assert _check_unit("-1*y") == "-y"
    assert _check_unit("2*z") == "2*z"


def test_expression_init_and_clear():
    """Test Expression initialization and clear method."""
    expr = Expression({('bx',): 1}, offset=5)
    assert expr.coefficient == {('bx',): 1}
    assert expr.offset == 5

    expr.clear()
    assert expr.coefficient == {}
    assert expr.offset == 0


def test_expression_arithmetic(expr_x, expr_y):
    """Test arithmetic operations on Expression objects."""
    # Addition
    res_add = expr_x + expr_y
    assert res_add.coefficient == {('bx',): 1, ('by',): 1}
    res_add_num = expr_x + 5
    assert res_add_num.offset == 5

    # Subtraction
    res_sub = expr_x - expr_y
    assert res_sub.coefficient == {('bx',): 1, ('by',): -1}

    # Multiplication
    res_mul = expr_x * expr_y
    assert res_mul.coefficient == {('bx', 'by'): 1}
    res_mul_num = expr_x * 3
    assert res_mul_num.coefficient == {('bx',): 3}

    # Division
    res_div = expr_x / 2
    assert res_div.coefficient == {('bx',): 0.5}

    # Power
    res_pow = (expr_x + 1) ** 2
    # (x+1)^2 = x^2 + 2x + 1. For a Binary var, x^2=x, so it's 3x+1
    assert res_pow.coefficient[('bx',)] == 3.0
    assert ('bx', 'bx') not in res_pow.coefficient
    assert res_pow.offset == 1

    # Test power > 2 raises error
    with pytest.raises(KaiwuError, match="Items higher than quadratic."):
        _ = (expr_x + expr_y) ** 3  # Use a non-binary expression to trigger

    # Negation
    res_neg = -expr_x
    assert res_neg.coefficient == {('bx',): -1}


def test_expression_reflected_arithmetic(expr_x):
    """Test reflected arithmetic (e.g., number + expression)."""
    res_radd = 5 + expr_x
    assert res_radd.coefficient == {('bx',): 1}
    assert res_radd.offset == 5

    res_rsub = 5 - expr_x
    assert res_rsub.coefficient == {('bx',): -1}
    assert res_rsub.offset == 5

    res_rmul = 3 * expr_x
    assert res_rmul.coefficient == {('bx',): 3}
    assert res_rmul.offset == 0


def test_expression_comparison(expr_x, expr_y):
    """Test comparison operators return ConstraintDefinition objects."""
    assert isinstance(expr_x == expr_y, ConstraintDefinition)
    assert isinstance(expr_x >= 5, ConstraintDefinition)
    assert isinstance(expr_x <= expr_y, ConstraintDefinition)
    assert isinstance(expr_x > 0, ConstraintDefinition)
    assert isinstance(expr_x < 1, ConstraintDefinition)


def test_expression_str_representation(expr_x, expr_y):
    """Test the __str__ method for various expressions."""
    res_str = str(expr_x + expr_y)
    assert "x" in res_str
    assert "y" in res_str
    assert "+" in res_str

    assert str(expr_x * expr_y) == "x*y"
    assert str(expr_x - 5) == "x-5"

    res_str_complex = str(2 * expr_x + 3 * expr_y - 4)
    assert "2*x" in res_str_complex
    assert "3*y" in res_str_complex
    assert "-4" in res_str_complex


def test_get_variables(expr_x, expr_y):
    """Test the get_variables method."""
    expr = 2 * expr_x * expr_y + expr_x - 1
    variables = expr.get_variables()
    assert isinstance(variables, tuple)
    assert 'bx' in variables
    assert 'by' in variables
    # Should be sorted
    assert variables == ('bx', 'by')


def test_get_max_deltas(expr_x, expr_y):
    """Test the get_max_deltas method."""
    expr = 2 * expr_x - 3 * expr_y + 4 * expr_x * expr_y
    neg_delta, pos_delta = expr.get_max_deltas()

    # For 'x': linear term is 2, quadratic is 4.
    # 1->0: -2 - 4*y. Max change is when y=0 -> -2.
    # 0->1: 2 + 4*y. Max change is when y=1 -> 6.
    assert pos_delta['bx'] == 6  # 2 (linear) + 4 (quad)
    assert neg_delta['bx'] == -2  # -2 (linear)

    # For 'y': linear term is -3, quadratic is 4.
    # 1->0: 3 - 4*x. Max change is when x=0 -> 3.
    # 0->1: -3 + 4*x. Max change is when x=1 -> 1.
    assert pos_delta['by'] == 1  # -3 (linear) + 4 (quad)
    assert neg_delta['by'] == 3  # 3 (linear)


def test_get_average_coefficient(expr_x, expr_y):
    """Test the get_average_coefficient method."""
    expr = 2 * expr_x - 4 * expr_y
    # Average of absolute values: (|2| + |-4|) / 2 = 3
    assert expr.get_average_coefficient() == 3.0

    # Test with no coefficients
    expr_no_coeff = Expression(offset=10)
    with pytest.raises(ZeroDivisionError):
        expr_no_coeff.get_average_coefficient()
