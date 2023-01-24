from util.get_functions import get_test_root_dir
from util.exceptions import (
    InvalidMetricValue,
)
from tests.test_helpers import create_file_df
from tests.utils.interpretation_functions_data import (
    INVALID_METRICS_TEST_DATA,
    SUCCESS_TEST_DATA,
    TEST_ROOT_DIR_TEST_DATA,
)
from glob import glob
import pytest


@pytest.mark.parametrize(
    "interpretation_func,data_frame,error_msg",
    INVALID_METRICS_TEST_DATA,
)
def test_interpretation_functions_invalid_metrics(
    interpretation_func, data_frame, error_msg
):
    """
    Test cases in which the interpretation functions should raise an InvalidMetricValue exception
    """

    with pytest.raises(InvalidMetricValue) as error:
        interpretation_func(data_frame)

    assert str(error.value) == error_msg


@pytest.mark.parametrize(
    "interpretation_func,data_frame,expected_result",
    SUCCESS_TEST_DATA,
)
def test_interpretation_functions_success(
    interpretation_func, data_frame, expected_result
):
    """
    Test cases in which the interpretation functions should return a valid measure
    """

    result = interpretation_func(data_frame)

    function_call = (
        f"{interpretation_func.__name__}({data_frame})"
    )

    assert (pytest.approx(result) == expected_result)

    assert 0 <= result <= 1.0, f"Expected: 0 <= {function_call} <= 1.0"


@pytest.mark.parametrize(
    "file_path,expected_value,language_extension", TEST_ROOT_DIR_TEST_DATA
)
def test_get_test_root_dir(file_path, expected_value, language_extension):
    """
    Test cases in which the get_test_root_dir function should return the series
    """

    json = glob(file_path)

    result = get_test_root_dir(create_file_df(json, language_extension))

    assert (
        int(result["tests"]) == expected_value
    ), f"Expected: {result} == {expected_value}"
