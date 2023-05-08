import core.measures_functions as ems_functions
from util.check_functions import (
    check_metric_value,
    check_metric_values,
)


def non_complex_files_density(data_frame, MINIMUM_COMPLEX_FILES_DENSITY_THRESHOLD: float = 0, MAXIMUM_COMPLEX_FILES_DENSITY_THRESHOLD: float = 10):
    """
    Calculates non-complex files density (em1).
    This function calculates non-complex files density measure (em1)
    used to assess the changeability quality subcharacteristic.

    This function gets the dataframe metrics
    and returns the non-complex files density measure (em1).
    """
    files_complexity = data_frame["complexity"]  # m1 metric
    files_functions = data_frame["functions"]  # m2 metric

    check_metric_values(files_complexity, "complexity")
    check_metric_values(files_functions, "functions")

    return ems_functions.calculate_em1(data={
        "complexity": files_complexity,
        "functions": files_functions,
    }, 
    MINIMUM_COMPLEX_FILES_DENSITY_THRESHOLD = MINIMUM_COMPLEX_FILES_DENSITY_THRESHOLD,
    MAXIMUM_COMPLEX_FILES_DENSITY_THRESHOLD = MAXIMUM_COMPLEX_FILES_DENSITY_THRESHOLD)


def commented_files_density(data_frame, MINIMUM_COMMENT_DENSITY_THRESHOLD: float = 10, MAXIMUM_COMMENT_DENSITY_THRESHOLD: float = 30):
    """
    Calculates commented files density (em2).

    This function gets the dataframe metrics
    and returns the commented files density measure (em2).
    """
    files_comment_lines_density = data_frame["comment_lines_density"]  # m4 metric

    check_metric_values(files_comment_lines_density, "comment_lines_density")

    return ems_functions.calculate_em2(data={
        "comment_lines_density": files_comment_lines_density,
    }, 
    MINIMUM_COMMENT_DENSITY_THRESHOLD = MINIMUM_COMMENT_DENSITY_THRESHOLD,
    MAXIMUM_COMMENT_DENSITY_THRESHOLD = MAXIMUM_COMMENT_DENSITY_THRESHOLD)


def absence_of_duplications(data_frame, MINIMUM_DUPLICATED_LINES_THRESHOLD: float = 0, MAXIMUM_DUPLICATED_LINES_THRESHOLD: float = 5.0):
    """
    Calculates duplicated files absence (em3).

    This function gets the dataframe metrics
    and returns the duplicated files absence measure (em3).
    """
    files_duplicated_lines_density = data_frame["duplicated_lines_density"]  # m5 metric

    check_metric_values(files_duplicated_lines_density, "duplicated_lines_density")

    return ems_functions.calculate_em3(data={
        "duplicated_lines_density": files_duplicated_lines_density
    },
    MINIMUM_DUPLICATED_LINES_THRESHOLD = MINIMUM_DUPLICATED_LINES_THRESHOLD,
    MAXIMUM_DUPLICATED_LINES_THRESHOLD = MAXIMUM_DUPLICATED_LINES_THRESHOLD)


def test_coverage(data_frame, MINIMUM_COVERAGE_THRESHOLD: float = 60, MAXIMUM_COVERAGE_THRESHOLD: float = 90):
    """
    Calculates test coverage (em6).

    This function gets the dataframe metrics
    and returns the test coverage measure (em6).
    """
    coverage = data_frame["coverage"]  # m6 metric

    check_metric_values(coverage, "coverage")

    return ems_functions.calculate_em6(data={
        "coverage": coverage
    },
    MINIMUM_COVERAGE_THRESHOLD = MINIMUM_COVERAGE_THRESHOLD,
    MAXIMUM_COVERAGE_THRESHOLD = MAXIMUM_COVERAGE_THRESHOLD)


def fast_test_builds(data_frame, MINIMUM_FAST_TEST_TIME_THRESHOLD: float = 0, MAXIMUM_FAST_TEST_TIME_THRESHOLD: float = 300000):
    """
    Calculates fast test builds (em5)
    This function gets the dataframe metrics
    and returns the fast test builds measure (em5).
    """
    test_execution_time = data_frame["test_execution_time"]
    tests = data_frame["tests"]

    check_metric_values(test_execution_time, "test_execution_time")
    check_metric_values(tests, "tests")

    return ems_functions.calculate_em5(data={
        "test_execution_time": test_execution_time,
        "tests": tests
    },
    MINIMUM_FAST_TEST_TIME_THRESHOLD = MINIMUM_FAST_TEST_TIME_THRESHOLD,
    MAXIMUM_FAST_TEST_TIME_THRESHOLD = MAXIMUM_FAST_TEST_TIME_THRESHOLD)


def passed_tests(data_frame, MINIMUM_PASSED_TESTS_THRESHOLD: float = 0, MAXIMUM_PASSED_TESTS_THRESHOLD: float = 1):
    """
    Calculates passed tests (em4)

    This function gets the dataframe metrics
    and returns the passed tests measure (em4).
    """
    tests = data_frame["tests"]  # m6 metrics
    test_errors = data_frame["test_errors"]  # m7 metrics
    test_failures = data_frame["test_failures"]  # m8 metrics

    check_metric_values(tests, "tests")
    check_metric_value(test_failures, "test_failures")
    check_metric_value(test_errors, "test_errors")

    return ems_functions.calculate_em4(data={
        "tests": tests,
        "test_errors": float(test_errors),
        "test_failures": float(test_failures),
    },
    MINIMUM_PASSED_TESTS_THRESHOLD = MINIMUM_PASSED_TESTS_THRESHOLD,
    MAXIMUM_PASSED_TESTS_THRESHOLD = MAXIMUM_PASSED_TESTS_THRESHOLD)
