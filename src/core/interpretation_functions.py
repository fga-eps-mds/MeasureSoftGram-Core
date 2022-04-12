from .exceptions import InvalidMetricValue, InvalidInterpretationFunctionArguments
import pandas as pd
import numpy as np


def check_arguments(data_frame):
    """
    Raises an InvalidInterpretationFunctionArguments exception if argument it's not a pandas.DataFrame.
    """

    if not isinstance(data_frame, pd.DataFrame):
        raise InvalidInterpretationFunctionArguments(
            "Expected data_frame to be a pandas.DataFrame"
        )


def check_number_of_files(number_of_files):
    """
    Raises an InvalidMetricValue exception if the number of files is lesser or equal than 0.
    """

    if number_of_files <= 0:
        raise InvalidMetricValue("The number of files is lesser or equal than 0")


def interpolate_series(series, x, y):
    """
    Interpolates a series using the given x and y values.

    This function interpolates a series using the given x and y values.
    """

    return [np.interp(item / 100, x, y) for item in series]


def create_coordinate_pair(min_threshhold, max_threshold, reverse_y=False):
    """
    Creates a pair of values.

    This function creates a pair of coordinates (x, y).
    """

    y = np.array([0, 1]) if reverse_y else np.array([1, 0])

    return np.array([min_threshhold, max_threshold]), y


def get_root_test_dir(data_frame):

    return data_frame.iloc[0]


def non_complex_files_density(data_frame):
    """
    Calculates non-complex files density (em1).

    This function calculates non-complex files density measure (em1)
    used to assess the changeability quality subcharacteristic.
    """

    check_arguments(data_frame)

    # files_complexity = m1 metric
    files_complexity = data_frame["complexity"].astype(float)
    # files_functions = m2 metric
    files_functions = data_frame["functions"].astype(float)
    # number_of_files = Tm3 metric
    number_of_files = len(data_frame)

    check_number_of_files(number_of_files)

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

    return sum(IF1) / number_of_files


def commented_files_density(data_frame):
    """
    Calculates commented files density (em2).

    This function calculates commented files density measure (em2)
    used to assess the changeability quality subcharacteristic.
    """

    MINIMUM_COMMENT_DENSITY_THRESHOLD = 10
    MAXIMUM_COMMENT_DENSITY_THRESHOLD = 30

    check_arguments(data_frame)

    # number_of_files = Tm3 metric
    number_of_files = len(data_frame)
    # files_comment_lines_density = m4 metric
    files_comment_lines_density = data_frame["comment_lines_density"].astype(float)

    check_number_of_files(number_of_files)

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

    return np.sum(em2i) / number_of_files


def absence_of_duplications(data_frame):
    """
    Calculates duplicated files absence (em3).

    This function calculates the duplicated files absence measure (em3)
    used to assess the changeability quality subcharacteristic.
    """

    DUPLICATED_LINES_THRESHOLD = 5.0

    check_arguments(data_frame)

    # files_duplicated_lines_density = m5 metric
    files_duplicated_lines_density = data_frame["duplicated_lines_density"].astype(
        float
    )
    # number_of_files = Tm3 metric
    number_of_files = len(data_frame)

    check_number_of_files(number_of_files)

    if files_duplicated_lines_density.sum() < 0:
        raise InvalidMetricValue(
            "The number of files duplicated lines density is lesser than 0"
        )

    x, y = create_coordinate_pair(0, DUPLICATED_LINES_THRESHOLD / 100)

    files_below_threshold = files_duplicated_lines_density[
        files_duplicated_lines_density <= DUPLICATED_LINES_THRESHOLD
    ]

    em3i = interpolate_series(files_below_threshold, x, y)

    return np.sum(em3i) / number_of_files


def test_coverage(data_frame):
    """
    Calculates test coverage (em6).

    This function calculates the test coverage measure (em6)
    used to assess the testing status subcharacteristic.
    """

    MINIMUM_COVERAGE_THRESHOLD = 60
    MAXIMUM_COVERAGE_THRESHOLD = 90

    check_arguments(data_frame)

    # number_of_files = m3 metric
    number_of_files = len(data_frame)
    # test_coverage = m6 metric
    test_coverage = data_frame["coverage"].astype(float)

    check_number_of_files(number_of_files)

    x, y = create_coordinate_pair(
        MINIMUM_COVERAGE_THRESHOLD / 100,
        MAXIMUM_COVERAGE_THRESHOLD / 100,
        reverse_y=True,
    )

    files_between_thresholds = test_coverage[
        test_coverage >= MINIMUM_COVERAGE_THRESHOLD
    ]

    em6i = interpolate_series(files_between_thresholds, x, y)

    return np.sum(em6i) / number_of_files


def fast_test_builds(data_frame):
    """
    Calculates fast test builds (em5)

    This function calculates the fast test builds measure (em5)
    used to assess the testing status subcharacteristic.
    """

    TEST_EXECUTION_TIME_THRESHOLD = 300000

    root_test = get_root_test_dir(data_frame)

    # test_execution_time = m9 metric
    test_execution_time = float(root_test["test_execution_time"])

    x, y = create_coordinate_pair(0, 1)

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
    root_test = get_root_test_dir(data_frame)
    # tests = m6 metrics
    tests = float(root_test["tests"])
    # test_errors = m7 metrics
    test_errors = float(root_test["test_errors"])
    # test_failures = m8 metrics
    test_failures = float(root_test["test_failures"])

    x, y = create_coordinate_pair(0, 1)

    if4i = (tests - (test_errors + test_failures)) / tests

    em4 = np.interp(if4i, x, y)

    return em4
