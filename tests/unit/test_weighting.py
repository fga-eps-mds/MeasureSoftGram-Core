from src.core.weighting import weighting_operation
import pytest

from src.core.exceptions import InvalidWeightSize


# @pytest.mark.parametrize()
# def test_weighting_operation():
#     list_whatever = function_asda()
#     tensor = create_sc_tensor(list_whatever, 1)
#     res = operation_ponderacao(tensor)
#     assert res == [[[0.23234132]], [[0.00202036]], [[0.30709461]]]


def test_weighting_operation():
    df = [0.30, 0.32, 0.12]
    weights = [0.30, 0.45, 0.25]
    res = weighting_operation(df, weights)

    assert pytest.approx(res.tolist()) == [0.09, 0.144, 0.03]


def test_weighting_operation_2():
    df = [0.40, 0.50, 0.10]
    weights = [0.30, 0.45, 0.25]
    res = weighting_operation(df, weights)

    assert pytest.approx(res.tolist()) == [0.12, 0.225, 0.025]


def test_same_sizes():
    df = [0.40, 0.50, 0.10]
    weights = [0.30, 0.45, 0.25]
    res = weighting_operation(df, weights)

    if len(df) == len(weights):
        assert pytest.approx(res.tolist()) == [0.12, 0.225, 0.025]


def test_different_sizes():
    with pytest.raises(InvalidWeightSize):
        df = [0.40, 0.40, 0.10, 0.10]
        weights = [0.30, 0.45, 0.25]
        if len(df) > len(weights):
            raise InvalidWeightSize


def test_different_sizes2():
    with pytest.raises(InvalidWeightSize):
        df = [0.40, 0.40, 0.10]
        weights = [0.30, 0.45, 0.15, 0.10]
        if len(df) < len(weights):
            raise InvalidWeightSize
