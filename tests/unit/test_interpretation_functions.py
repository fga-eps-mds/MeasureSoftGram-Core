from src.core.interpretation_functions import (
    non_complex_files_density,
    commented_files_density,
    absence_of_duplications,
    test_coverage,
)
from src.core.exceptions import (
    InvalidMetricValue,
    InvalidInterpretationFunctionArguments,
)
from tests.test_helpers import create_file_df
import pandas as pd
from glob import glob
import pytest


INVALID_METRICS_TEST_DATA = [
    (
        non_complex_files_density,
        "tests/unit/data/zero_number_of_files.json",
        "The number of files is lesser or equal than 0",
    ),
    (
        non_complex_files_density,
        "tests/unit/data/zero_number_of_functions.json",
        "The number of functions of all files is lesser or equal than 0",
    ),
    (
        non_complex_files_density,
        "tests/unit/data/zero_cyclomatic_complexity.json",
        "The cyclomatic complexity of all files is lesser or equal than 0",
    ),
    (
        commented_files_density,
        "tests/unit/data/zero_number_of_files.json",
        "The number of files is lesser or equal than 0",
    ),
    (
        absence_of_duplications,
        "tests/unit/data/zero_number_of_files.json",
        "The number of files is lesser or equal than 0",
    ),
    (
        test_coverage,
        "tests/unit/data/zero_number_of_files.json",
        "The number of files is lesser or equal than 0",
    ),
]


SUCCESS_TEST_DATA = [
    (
        non_complex_files_density,
        "tests/unit/data/fga-eps-mds_2021-2-SiGeD-Frontend-03-15-2022-23_57_08.json",
        0.688622754491018,
    ),
    (
        non_complex_files_density,
        "tests/unit/data/fga-eps-mds-2020_2-Projeto-Kokama-Usuario-17-04-2021.json",
        0.0,
    ),
    (
        non_complex_files_density,
        "tests/unit/data/fga-eps-mds-2020_2-Lend.it-Raleway-user-13-04-2021.json",
        0.6428571428571429,
    ),
    (
        commented_files_density,
        "tests/unit/data/fga-eps-mds-2020_2-Projeto-Kokama-Usuario-17-04-2021.json",
        0.0,
    ),
    (
        commented_files_density,
        "tests/unit/data/fga-eps-mds_2021-2-SiGeD-Frontend-03-15-2022-23_57_08.json",
        0.0050299401197604785,
    ),
    (
        commented_files_density,
        "tests/unit/data/fga-eps-mds-2020_2-Lend.it-Raleway-user-13-04-2021.json",
        0.0,
    ),
    (
        absence_of_duplications,
        "tests/unit/data/fga-eps-mds_2021-2-SiGeD-Frontend-03-15-2022-23_57_08.json",
        0.9101796407185628,
    ),
    (
        absence_of_duplications,
        "tests/unit/data/fga-eps-mds-2020_2-Projeto-Kokama-Usuario-17-04-2021.json",
        1.0,
    ),
    (
        absence_of_duplications,
        "tests/unit/data/fga-eps-mds-2020_2-Lend.it-Raleway-user-13-04-2021.json",
        1.0,
    ),
    (
        test_coverage,
        "tests/unit/data/fga-eps-mds_2021-2-SiGeD-Frontend-03-15-2022-23_57_08.json",
        0.0,
    ),
    (
        test_coverage,
        "tests/unit/data/between_zero_and_one_coverage.json",
        0.545454,
    ),
    (
        test_coverage,
        "tests/unit/data/zero_cyclomatic_complexity.json",
        1.0,
    ),
]


INVALID_ARGUMENTS_TEST_DATA = [
    (non_complex_files_density, None),
    (non_complex_files_density, False),
    (
        non_complex_files_density,
        pd.Series(data={"a": 1, "b": 2, "c": 3}, index=["a", "b", "c"]),
    ),
    (commented_files_density, None),
    (commented_files_density, False),
    (
        commented_files_density,
        pd.Series(data={"a": 1, "b": 2, "c": 3}, index=["a", "b", "c"]),
    ),
    (absence_of_duplications, None),
    (absence_of_duplications, False),
    (
        absence_of_duplications,
        pd.Series(data={"a": 1, "b": 2, "c": 3}, index=["a", "b", "c"]),
    ),
    (test_coverage, None),
    (test_coverage, False),
    (
        test_coverage,
        pd.Series(data={"a": 1, "b": 2, "c": 3}, index=["a", "b", "c"]),
    ),
]


@pytest.mark.parametrize(
    "interpretation_func,file_path,error_msg", INVALID_METRICS_TEST_DATA
)
def test_interpretation_functions_invalid_metrics(
    interpretation_func, file_path, error_msg
):
    """
    Test cases in which the interpretation functions should raise an InvalidMetricValue exception
    """

    json = glob(file_path)

    with pytest.raises(InvalidMetricValue) as error:
        interpretation_func(create_file_df(json))

    function_call = (
        f"{interpretation_func.__name__}(create_file_df('{file_path.split('/')[-1]}'))"
    )

    assert_msg = (
        f"Expected: {function_call} to raise an InvalidMetricValue('{error_msg}')"
    )

    assert str(error.value) == error_msg, assert_msg


@pytest.mark.parametrize(
    "interpretation_func,file_path,expected_result", SUCCESS_TEST_DATA
)
def test_interpretation_functions_success(
    interpretation_func, file_path, expected_result
):
    """
    Test cases in which the interpretation functions should return a valid measure
    """

    # assert expected_result == 1.0
    json = glob(file_path)

    result = interpretation_func(create_file_df(json))

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
