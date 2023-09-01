import pytest

from tests.utils.aggregated_normalized_measures_data import (
    INVALID_METRICS_TEST_DATA,
    INVALID_THRESHOLD_TEST_DATA,
    SUCCESS_TEST_DATA,
)
from util.exceptions import InvalidMetricValue, InvalidThresholdValue


@pytest.mark.parametrize(
    "aggregated_normalized_measure,data_frame,error_msg",
    INVALID_METRICS_TEST_DATA,
)
def test_aggregated_normalized_measures_invalid_metrics(
    aggregated_normalized_measure, data_frame, error_msg
):
    """
    Test cases in which the interpretation functions should raise an InvalidMetricValue exception
    """

    with pytest.raises(InvalidMetricValue) as error:
        aggregated_normalized_measure(data_frame)

    assert str(error.value) == error_msg


@pytest.mark.parametrize(
    "aggregated_normalized_measure,data_frame,expected_result",
    SUCCESS_TEST_DATA,
)
def test_aggregated_normalized_measures_success(
    aggregated_normalized_measure, data_frame, expected_result
):
    """
    Test cases in which the interpretation functions should return a valid measure
    """

    result = aggregated_normalized_measure(data_frame)

    function_call = f"{aggregated_normalized_measure.__name__}({data_frame})"

    assert pytest.approx(result) == expected_result

    assert 0 <= result <= 1.0, f"Expected: 0 <= {function_call} <= 1.0"


@pytest.mark.parametrize(
    "aggregated_normalized_measure,params,error_msg",
    INVALID_THRESHOLD_TEST_DATA,
)
def test_aggregated_normalized_measures_invalid_thresholds(
    aggregated_normalized_measure, params, error_msg
):
    """
    Test cases in which the interpretation functions should return a valid measure
    """
    with pytest.raises(InvalidThresholdValue) as error:
        aggregated_normalized_measure(**params)

    assert str(error.value) == error_msg
