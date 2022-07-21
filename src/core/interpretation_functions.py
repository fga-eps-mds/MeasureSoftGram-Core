from .exceptions import InvalidMetricValue, InvalidInterpretationFunctionArguments
import pandas as pd
import numpy as np
import math


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


def check_metric_value(metric_value, metric):
    try:
        if metric_value is None or math.isnan(float(metric_value)):
            raise InvalidMetricValue(f'"{metric}" has an invalid metric value')
    except (ValueError, TypeError):
        raise InvalidMetricValue(f'"{metric}" has an invalid metric value')


def check_metric_values(metric_values, metric):
    for value in metric_values:
        check_metric_value(value, metric)


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


def get_files_data_frame(data_frame):
    """
    Returns a data frame with files data.

    This function returns a data frame with files data.
    """

    return data_frame[
        (data_frame["qualifier"] == "FIL") & (data_frame["ncloc"].astype(float) > 0)
    ]


def get_test_root_dir(data_frame):

    dirs = data_frame[data_frame["qualifier"] == "DIR"]

    return dirs.loc[dirs["tests"].astype(float).idxmax()]


def non_complex_files_density(data_frame):
    """
    Calculates non-complex files density (em1).

    This function calculates non-complex files density measure (em1)
    used to assess the changeability quality subcharacteristic.
    """

    COMPLEX_FILES_DENSITY_THRESHOLD = 10

    check_arguments(data_frame)

    files_df = get_files_data_frame(data_frame)

    # files_complexity = m1 metric
    files_complexity = files_df["complexity"].astype(float)
    # files_functions = m2 metric
    files_functions = files_df["functions"].astype(float)
    # number_of_files = Tm3 metric
    number_of_files = len(files_df)

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

    # Change to hardcoded 10
    # m0 = np.median(files_complexity / files_functions)

    x, y = create_coordinate_pair(0, COMPLEX_FILES_DENSITY_THRESHOLD)

    files_in_thresholds_df = (files_complexity / files_functions) <= COMPLEX_FILES_DENSITY_THRESHOLD

    IF1 = np.interp(list(files_in_thresholds_df[(files_functions > 0)]), x, y)

    em1 = sum(IF1) / number_of_files

    return em1


def commented_files_density(data_frame):
    """
    Calculates commented files density (em2).

    This function calculates commented files density measure (em2)
    used to assess the changeability quality subcharacteristic.
    """

    MINIMUM_COMMENT_DENSITY_THRESHOLD = 10
    MAXIMUM_COMMENT_DENSITY_THRESHOLD = 30

    check_arguments(data_frame)

    files_df = get_files_data_frame(data_frame)

    # number_of_files = Tm3 metric
    number_of_files = len(files_df)
    # files_comment_lines_density = m4 metric
    files_comment_lines_density = files_df["comment_lines_density"].astype(float)

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


def absence_of_duplications(data_frame):
    """
    Calculates duplicated files absence (em3).

    This function calculates the duplicated files absence measure (em3)
    used to assess the changeability quality subcharacteristic.
    """

    DUPLICATED_LINES_THRESHOLD = 5.0

    check_arguments(data_frame)

    files_df = get_files_data_frame(data_frame)

    # files_duplicated_lines_density = m5 metric
    files_duplicated_lines_density = files_df["duplicated_lines_density"].astype(float)
    # number_of_files = Tm3 metric
    number_of_files = len(files_df)

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

    # number_of_files = m3 metric
    number_of_files = len(files_df)
    # test_coverage = m6 metric
    test_coverage = files_df["coverage"].astype(float)

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

    # test_execution_time = m9 metric
    test_execution_time = float(root_test["test_execution_time"])

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

    # tests = m6 metrics
    tests = float(root_test["tests"])
    # test_errors = m7 metrics
    test_errors = float(root_test["test_errors"])
    # test_failures = m8 metrics
    test_failures = float(root_test["test_failures"])

    x, y = create_coordinate_pair(0, 1, reverse_y=True)

    if4i = (tests - (test_errors + test_failures)) / tests

    em4 = np.interp(if4i, x, y)

    return em4
