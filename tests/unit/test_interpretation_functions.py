from util.get_functions import get_test_root_dir
from util.exceptions import (
    InvalidMetricValue,
    InvalidInterpretationFunctionArguments,
)
from tests.test_helpers import create_file_df
from tests.utils.interpretation_functions_data import (
    INVALID_METRICS_TEST_DATA,
    SUCCESS_TEST_DATA,
    INVALID_ARGUMENTS_TEST_DATA,
    TEST_ROOT_DIR_TEST_DATA,
)
import pandas as pd
from glob import glob
import pytest


@pytest.mark.parametrize(
    "interpretation_func,file_path,error_msg,language_extension",
    INVALID_METRICS_TEST_DATA,
)
def test_interpretation_functions_invalid_metrics(
    interpretation_func, file_path, error_msg, language_extension
):
    """
    Test cases in which the interpretation functions should raise an InvalidMetricValue exception
    """

    json = glob(file_path)

    with pytest.raises(InvalidMetricValue) as error:
        interpretation_func(create_file_df(json, language_extension))

    function_call = (
        f"{interpretation_func.__name__}(create_file_df('{file_path.split('/')[-1]}'))"
    )

    assert_msg = (
        f"Expected: {function_call} to raise an InvalidMetricValue('{error_msg}')"
    )

    assert str(error.value) == error_msg, assert_msg


@pytest.mark.parametrize(
    "interpretation_func,file_path,expected_result,language_extension",
    SUCCESS_TEST_DATA,
)
def test_interpretation_functions_success(
    interpretation_func, file_path, expected_result, language_extension
):
    """
    Test cases in which the interpretation functions should return a valid measure
    """

    # assert expected_result == 1.0
    json = glob(file_path)

    result = interpretation_func(create_file_df(json, language_extension))

    function_call = (
        f"{interpretation_func.__name__}(create_file_df('{file_path.split('/')[-1]}'))"
    )

    assert (
        pytest.approx(result) == expected_result
    ), f"Expected: {function_call} == {expected_result}"

    assert 0 <= result <= 1.0, f"Expected: 0 <= {function_call} <= 1.0"


@pytest.mark.parametrize("interpretation_func,data_frame", INVALID_ARGUMENTS_TEST_DATA)
def test_non_complex_files_density_error_arguments(interpretation_func, data_frame):
    """
    Test cases in which the interpretation functions should raise an InvalidInterpretationFunctionArguments exception
    """

    with pytest.raises(InvalidInterpretationFunctionArguments) as error:
        interpretation_func(data_frame)

    str_value = "pd.Series()" if isinstance(data_frame, pd.Series) else data_frame

    function_call = f"{interpretation_func.__name__}({str_value})"

    error_msg = "Expected data_frame to be a pandas.DataFrame"

    assert (
        str(error.value) == error_msg
    ), f"Expected: {function_call} to raise an InvalidInterpretationFunctionArguments"


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
