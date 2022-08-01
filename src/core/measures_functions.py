import numpy as np
import pandas as pd
from typing import Dict

from src.util.exceptions import InvalidMetricValue
from src.util.get_functions import create_coordinate_pair


def interpolate_series(series, x, y):
    """
    Interpolates a series using the given x and y values.

    This function interpolates a series using the given x and y values.
    """

    return [np.interp(item / 100, x, y) for item in series]


def resolve_metric_list_parameter(metric):
    """
    Resolves the metric list parameter to calculate a measure

    This functions converts the metric parameter to a pandas Series if it is a list (CalculateSpecificMeasure endpoint)
    otherwise it just returns the metric - already a pandas Series (Analysis endpoint).
    """
    return pd.Series(metric, dtype=np.float64) if isinstance(metric, list) else metric


def calculate_em1(data: Dict):
    """
    Calculates non-complex files density (em1).

    This function calculates non-complex files density measure (em1)
    used to assess the changeability quality sub characteristic.
    """
    files_complexity = resolve_metric_list_parameter(data["complexity"])
    files_functions = resolve_metric_list_parameter(data["functions"])
    number_of_files = data["number_of_files"]

    COMPLEX_FILES_DENSITY_THRESHOLD = 10

    if files_complexity.sum() <= 0:
        raise InvalidMetricValue(
            "The cyclomatic complexity of all files is lesser or equal than 0"
        )

    if files_functions.sum() <= 0:
        raise InvalidMetricValue(
            "The number of functions of all files is lesser or equal than 0"
        )

    x, y = create_coordinate_pair(0, COMPLEX_FILES_DENSITY_THRESHOLD)

    files_in_thresholds_df = (files_complexity / files_functions) <= COMPLEX_FILES_DENSITY_THRESHOLD
    IF1 = np.interp(list(files_in_thresholds_df[(files_functions > 0)]), x, y)
    em1 = sum(IF1) / number_of_files
    return em1


def calculate_em2(data: Dict):
    """
    Calculates commented files density (em2).

    This function calculates commented files density measure (em2)
    used to assess the changeability quality sub characteristic.
    """
    number_of_files = data["number_of_files"]
    files_comment_lines_density = resolve_metric_list_parameter(data["comment_lines_density"])

    MINIMUM_COMMENT_DENSITY_THRESHOLD = 10
    MAXIMUM_COMMENT_DENSITY_THRESHOLD = 30

    if files_comment_lines_density.sum() < 0:
        raise InvalidMetricValue(
            "The number of files comment lines density is lesser than 0"
        )

    x, y = create_coordinate_pair(
        MINIMUM_COMMENT_DENSITY_THRESHOLD / 100, MAXIMUM_COMMENT_DENSITY_THRESHOLD / 100
    )

    files_between_thresholds = files_comment_lines_density[
        files_comment_lines_density.between(
            MINIMUM_COMMENT_DENSITY_THRESHOLD,
            MAXIMUM_COMMENT_DENSITY_THRESHOLD,
            inclusive="both",
        )
    ]

    em2i = interpolate_series(files_between_thresholds, x, y)
    em2 = np.sum(em2i) / number_of_files
    return em2


def calculate_em3(data: Dict):
    """
    Calculates duplicated files absence (em3).

    This function calculates the duplicated files absence measure (em3)
    used to assess the changeability quality sub characteristic.
    """
    number_of_files = data["number_of_files"]
    files_duplicated_lines_density = resolve_metric_list_parameter(data["duplicated_lines_density"])

    DUPLICATED_LINES_THRESHOLD = 5.0

    if files_duplicated_lines_density.sum() < 0:
        raise InvalidMetricValue(
            "The number of files duplicated lines density is lesser than 0"
        )

    x, y = create_coordinate_pair(0, DUPLICATED_LINES_THRESHOLD / 100)

    files_below_threshold = files_duplicated_lines_density[
        files_duplicated_lines_density <= DUPLICATED_LINES_THRESHOLD
    ]

    em3i = interpolate_series(files_below_threshold, x, y)
    em3 = np.sum(em3i) / number_of_files
    return em3


def calculate_em4(data: Dict[str, float]):
    """
    Calculates passed tests (em4)

    This function calculates the passed tests measure (em4)
    used to assess the testing status sub characteristic.
    """
    number_of_tests = data["tests"]
    number_of_test_errors = data["test_errors"]
    number_of_test_failures = data["test_failures"]

    x, y = create_coordinate_pair(0, 1, reverse_y=True)

    number_of_fail_tests = number_of_test_errors + number_of_test_failures
    if4i = (number_of_tests - number_of_fail_tests) / number_of_tests
    return np.interp(if4i, x, y)


def calculate_em5(data: Dict[str, float]):
    """
    Calculates fast test builds (em5)

    This function calculates the fast test builds measure (em5)
    used to assess the testing status sub characteristic.
    """
    test_execution_time = data["test_execution_time"]

    TEST_EXECUTION_TIME_THRESHOLD = 300000

    x, y = create_coordinate_pair(0, 1, reverse_y=True)

    em5 = 0
    if test_execution_time < TEST_EXECUTION_TIME_THRESHOLD:
        if5i = test_execution_time / TEST_EXECUTION_TIME_THRESHOLD
        em5 = np.interp(if5i, x, y)
    return em5


def calculate_em6(data: Dict):
    """
    Calculates test coverage (em6).

    This function calculates the test coverage measure (em6)
    used to assess the testing status sub characteristic.
    """
    coverage = resolve_metric_list_parameter(data["coverage"])
    number_of_files = data["number_of_files"]

    MINIMUM_COVERAGE_THRESHOLD = 60
    MAXIMUM_COVERAGE_THRESHOLD = 90

    x, y = create_coordinate_pair(
        MINIMUM_COVERAGE_THRESHOLD / 100,
        MAXIMUM_COVERAGE_THRESHOLD / 100,
        reverse_y=True,
    )

    files_between_thresholds = coverage[coverage >= MINIMUM_COVERAGE_THRESHOLD]
    em6i = interpolate_series(files_between_thresholds, x, y)
    em6 = np.sum(em6i) / number_of_files
    return em6


def calculate_em7(data: Dict):
    """
    Calculates test coverage (em6).

    This function calculates team throughput measure.
    """
    number_of_resolved_issues = data["number_of_resolved_issues"]
    number_of_issues = data["total_number_of_issues"]

    MIN_THRESHOLD = 0
    MAX_THRESHOLD = 1

    x, y = create_coordinate_pair(
        MIN_THRESHOLD,
        MAX_THRESHOLD,
        reverse_y=True
    )

    if7 = np.divide(number_of_resolved_issues, number_of_issues)
    em7 = np.interp(if7, x, y)

    return em7


def calculate_em8(data: Dict[str, float]):
    """
    Calculates CI feedback time measure (em8)

    This function calculates average feedback time from CI system.
    The calculation will be the feedback time for every build
    divided by total builds
    """
    denominator = data['number_of_build_pipelines_in_the_last_x_days']
    numerator = data['runtime_sum_of_build_pipelines_in_the_last_x_days']

    if not denominator:
        raise InvalidMetricValue("The number of build pipelines cannot be 0")

    return numerator / denominator
