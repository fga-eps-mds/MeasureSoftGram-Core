from src.core.interpretation_functions import non_complex_files_density
from src.core.exceptions import InvalidMetricValue, InvalidInterpretationFunctionArguments
from tests.test_helpers import create_file_df
import pandas as pd
from glob import glob
import pytest


ERROR_TEST_DATA = [
    ('tests/unit/data/zero_number_of_files.json', 'The number of files is lesser or equal than 0'),
    ('tests/unit/data/zero_number_of_functions.json', 'The number of functions of all files is lesser or equal than 0'),
    ('tests/unit/data/zero_cyclomatic_complexity.json', 'The cyclomatic complexity of all files is lesser or equal than 0')
]


SUCCESS_TEST_DATA = [
    ('tests/unit/data/fga-eps-mds_2021-2-SiGeD-Frontend-03-15-2022-23_57_08.json', 0.688622754491018),
    ('tests/unit/data/fga-eps-mds-2020_2-Projeto-Kokama-Usuario-17-04-2021.json', 1.0)
]


INVALID_ARGUMENTS_TEST_DATA = [
    None,
    False,
    pd.Series(data={'a': 1, 'b': 2, 'c': 3}, index=['a', 'b', 'c'])
]


@pytest.mark.parametrize("file_path,error_msg", ERROR_TEST_DATA)
def test_non_complex_files_density_error_metrics(file_path, error_msg):
    json = glob(file_path)

    with pytest.raises(InvalidMetricValue) as error:
        non_complex_files_density(create_file_df(json))

    assert str(error.value) == error_msg


@pytest.mark.parametrize("file_path,expected_result", SUCCESS_TEST_DATA)
def test_non_complex_files_density(file_path, expected_result):
    json = glob(file_path)

    result = non_complex_files_density(create_file_df(json))

    assert result == expected_result
    assert 0 <= result <= 1.0


@pytest.mark.parametrize("data_frame", INVALID_ARGUMENTS_TEST_DATA)
def test_non_complex_files_density_error_arguments(data_frame):

    with pytest.raises(InvalidInterpretationFunctionArguments) as error:
        non_complex_files_density(data_frame)

    assert str(error.value) == 'Expected data_frame to be a pandas.DataFrame'
