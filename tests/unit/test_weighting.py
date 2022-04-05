from src.core.weighting import weighting_operation
import pytest

from src.core.exceptions import InvalidEqualityOfWeightAndValues, InvalidWeightingOperation


# @pytest.mark.parametrize()
# def test_weighting_operation():
#     list_whatever = function_asda()
#     tensor = create_sc_tensor(list_whatever, 1)
#     res = operation_ponderacao(tensor)
#     assert res == [[[0.23234132]], [[0.00202036]], [[0.30709461]]]


INVALID_WEIGHTING_OPERATION = [
    ([0.30, 0.32, 0.12], [0.30, 0.45, 0.25], [0.90, 0.18, 0.30]),
    ([0.40, 0.50, 0.10], [0.30, 0.45, 0.25], [0.20, 0.20, 0.25]),
    ([0.20, 0.30, 0.50], [0.25, 0.40, 0.35], [0.50, 0.12, 0.175]),
]


VALID_WEIGHTING_OPERATION = [
    ([0.30, 0.32, 0.12], [0.30, 0.45, 0.25], [0.09, 0.144, 0.03]),
    ([0.40, 0.50, 0.10], [0.30, 0.45, 0.25], [0.12, 0.225, 0.025]),
    ([0.20, 0.30, 0.50], [0.25, 0.40, 0.35], [0.05, 0.12, 0.175]),
]


VALID_SIZES = [
    ([0.30], [1.00]),
    ([0.30, 0.32], [0.30, 0.70]),
    ([0.30, 0.32, 0.12], [0.30, 0.45, 0.25]),
    ([0.30, 0.32, 0.02, 0.10], [0.30, 0.45, 0.15, 0.10]),
    ([0.30, 0.32, 0.02, 0.05, 0.05], [0.30, 0.45, 0.15, 0.05, 0.05]),
]


INVALID_SIZES = [
    ([0.30], [0.30, 0.70]),
    ([0.30, 0.45], [1.00]),
    ([0.30, 0.32], [0.30, 0.45, 0.25]),
    ([0.30, 0.32, 0.12], [0.30, 0.70]),
    ([0.30, 0.32, 0.02], [0.30, 0.45, 0.15, 0.10]),
    ([0.30, 0.32, 0.02, 0.10], [0.30, 0.45, 0.25]),
]


@pytest.mark.parametrize("values, weights, res", VALID_WEIGHTING_OPERATION)
def test_valid_weighting_operation(values, weights, res):
    """
    Test cases in which the weighting operation should return a valid result
    """

    check = weighting_operation(values, weights)
    assert pytest.approx(check.tolist()) == res


@pytest.mark.parametrize("values, weights, res", INVALID_WEIGHTING_OPERATION)
def test_invalid_weighting_operation(values, weights, res):
    """
    Test cases in which the weighting operation returns a invalid result
    """

    with pytest.raises(InvalidWeightingOperation):
        check = weighting_operation(values, weights)
        if pytest.approx(check.tolist()) != res:
            raise InvalidWeightingOperation


@pytest.mark.parametrize("values, weights", VALID_SIZES)
def test_same_sizes(values, weights):
    """
    Test cases in which the size of the weight and values are the same
    """

    assert len(values) == len(weights)


@pytest.mark.parametrize("values, weights", INVALID_SIZES)
def test_different_sizes(values, weights):
    """
    Test cases in which the size of the weight and values are not the same
    """

    with pytest.raises(InvalidEqualityOfWeightAndValues):
        if len(values) != len(weights):
            raise InvalidEqualityOfWeightAndValues
