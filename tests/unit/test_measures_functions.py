import pytest

from tests.utils.measures_functions import INVALID_TRESHOLD_DATA
from util.exceptions import InvalidThresholdValue


@pytest.mark.parametrize("func,params,error_msg", INVALID_TRESHOLD_DATA)
def test_measure_funcions_invalid_threshold(func, params, error_msg):
    """
    Test cases in which the measure functions should raise an InvalidThresholdValue exception
    """
    with pytest.raises(InvalidThresholdValue) as error:
        func(**params)

    assert str(error.value) == error_msg
