from src.core.interpretation_functions import non_complex_files_density
from src.core.exceptions import InvalidMetricValue
from tests.test_helpers import create_file_df
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


@pytest.mark.parametrize("file_path,error_msg", ERROR_TEST_DATA)
def test_non_complex_files_density_error(file_path, error_msg):
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
