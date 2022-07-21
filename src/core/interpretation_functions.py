from src.util.check_functions import (
    check_arguments,
    check_metric_value,
    check_metric_values,
    check_number_of_files
)
from src.util.get_functions import (
    get_files_data_frame,
    get_test_root_dir,
    create_coordinate_pair
)
from src.util.exceptions import InvalidMetricValue
import numpy as np
import pandas as pd


def interpolate_series(series, x, y):
    """
    Interpolates a series using the given x and y values.
    """

    return [np.interp(item / 100, x, y) for item in series]


def non_complex_files_density(data_frame):
    """
    Calculates non-complex files density (em1).

    This function calculates non-complex files density measure (em1)
    used to assess the changeability quality subcharacteristic.
    """

    check_arguments(data_frame)
    files_df = get_files_data_frame(data_frame)

    files_complexity = files_df["complexity"].astype(float) # m1 metric
    files_functions = files_df["functions"].astype(float) # m2 metric
    number_of_files = len(files_df) # Tm3 metric

    check_number_of_files(number_of_files)
    check_metric_values(files_complexity, "complexity")
    check_metric_values(files_functions, "functions")

    if files_complexity.sum() <= 0:
        raise InvalidMetricValue(
            "The cyclomatic complexity of all files is lesser or equal than 0"
        )

    if files_functions.sum() <= 0:
        raise InvalidMetricValue(
            "The number of functions of all files is lesser or equal than 0"
        )

    m0 = np.median(files_complexity / files_functions)
    x, y = create_coordinate_pair(0, m0)
    files_in_thresholds_df = (files_complexity / files_functions) <= m0
    IF1 = np.interp(list(files_in_thresholds_df[(files_functions > 0)]), x, y)
    em1 = sum(IF1) / number_of_files

    return em1


def commented_files_density(data_frame: pd.DataFrame):
    """
    Calculates commented files density (em2).

    This function calculates commented files density measure (em2)
    used to assess the changeability quality subcharacteristic.
    """

    MINIMUM_COMMENT_DENSITY_THRESHOLD = 10
    MAXIMUM_COMMENT_DENSITY_THRESHOLD = 30

    check_arguments(data_frame)
    files_df = get_files_data_frame(data_frame)

    number_of_files = len(files_df) # Tm3 metric
    files_comment_lines_density = files_df["comment_lines_density"].astype(float) # m4 metric

    check_number_of_files(number_of_files)
    check_metric_values(files_comment_lines_density, "comment_lines_density")

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


def absence_of_duplications(data_frame: pd.DataFrame):
    """
    Calculates duplicated files absence (em3).

    This function calculates the duplicated files absence measure (em3)
    used to assess the changeability quality subcharacteristic.
    """

    DUPLICATED_LINES_THRESHOLD = 5.0

    check_arguments(data_frame)
    files_df = get_files_data_frame(data_frame)

    files_duplicated_lines_density = files_df["duplicated_lines_density"].astype(float) # m5 metric
    number_of_files = len(files_df) # Tm3 metric

    check_number_of_files(number_of_files)
    check_metric_values(files_duplicated_lines_density, "duplicated_lines_density")

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


def test_coverage(data_frame):
    """
    Calculates test coverage (em6).

    This function calculates the test coverage measure (em6)
    used to assess the testing status subcharacteristic.
    """

    MINIMUM_COVERAGE_THRESHOLD = 60
    MAXIMUM_COVERAGE_THRESHOLD = 90

    check_arguments(data_frame)
    files_df = get_files_data_frame(data_frame)

    number_of_files = len(files_df) # m3 metric
    test_coverage = files_df["coverage"].astype(float) # m6 metric
    
    check_number_of_files(number_of_files)
    check_metric_values(test_coverage, "coverage")
    
    x, y = create_coordinate_pair(
        MINIMUM_COVERAGE_THRESHOLD / 100,
        MAXIMUM_COVERAGE_THRESHOLD / 100,
        reverse_y=True,
    )

    files_between_thresholds = test_coverage[
        test_coverage >= MINIMUM_COVERAGE_THRESHOLD
    ]

    em6i = interpolate_series(files_between_thresholds, x, y)
    em6 = np.sum(em6i) / number_of_files

    return em6


def fast_test_builds(data_frame):
    """
    Calculates fast test builds (em5)

    This function calculates the fast test builds measure (em5)
    used to assess the testing status subcharacteristic.
    """

    TEST_EXECUTION_TIME_THRESHOLD = 300000
    root_test = get_test_root_dir(data_frame)
    check_metric_value(root_test["test_execution_time"], "test_execution_time")
    test_execution_time = float(root_test["test_execution_time"])  # m9 metric
    x, y = create_coordinate_pair(0, 1, reverse_y=True)
    em5 = 0

    if test_execution_time < TEST_EXECUTION_TIME_THRESHOLD:
        if5i = test_execution_time / TEST_EXECUTION_TIME_THRESHOLD
        em5 = np.interp(if5i, x, y)

    return em5


def passed_tests(data_frame):
    """
    Calculates passed tests (em4)

    This function calculates the passed tests measure (em4)
    used to assess the testing status subcharacteristic.
    """
    root_test = get_test_root_dir(data_frame)

    check_metric_value(root_test["tests"], "tests")
    check_metric_value(root_test["test_errors"], "test_errors")
    check_metric_value(root_test["test_failures"], "test_failures")

    tests = float(root_test["tests"]) # m6 metrics
    test_errors = float(root_test["test_errors"]) # m7 metrics
    test_failures = float(root_test["test_failures"]) # m8 metrics

    x, y = create_coordinate_pair(0, 1, reverse_y=True)
    if4i = (tests - (test_errors + test_failures)) / tests
    em4 = np.interp(if4i, x, y)

    return em4


def team_throughput(data_frame: pd.DataFrame):
    """
    Calculates team throughput measure.

    This function is used to calculate the ratio between the number
    of issues resolved and the total number of issues given a time frame,
    A.K.A. team throughput.
    """
    check_arguments(data_frame)

    pass