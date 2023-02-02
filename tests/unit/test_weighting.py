from core.weighting import weighting_operation
from util.exceptions import ValuesAndWeightsOfDifferentSizes
from tests.utils.weighting_data import (
    VALID_WEIGHTING_OPERATION,
    INVALID_SIZES,
)

import pytest


@pytest.mark.parametrize("values, weights, res", VALID_WEIGHTING_OPERATION)
def test_valid_weighting_operation(values, weights, res):
    """
    Test cases in which the weighting operation should return a valid result
    """

    result = weighting_operation(values, weights)
    assert pytest.approx(result.tolist()) == res


@pytest.mark.parametrize("values, weights", INVALID_SIZES)
def test_different_sizes(values, weights):
    """
    Test cases in which the size of the weight and values are not the same
    """

    with pytest.raises(ValuesAndWeightsOfDifferentSizes) as error:
        weighting_operation(values, weights)

    assert str(error.value) == 'The length of weight and values are not equal'
