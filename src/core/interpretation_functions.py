import pandas as pd

import core.measures_functions as ems_functions
from util.check_functions import (
    check_metric_value,
    check_metric_values,
)


def non_complex_files_density(data_frame):
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
    })


def commented_files_density(data_frame):
    """
    Calculates commented files density (em2).

    This function gets the dataframe metrics
    and returns the commented files density measure (em2).
    """
    files_comment_lines_density = data_frame["comment_lines_density"]  # m4 metric

    check_metric_values(files_comment_lines_density, "comment_lines_density")

    return ems_functions.calculate_em2(data={
        "comment_lines_density": files_comment_lines_density,
    })


def absence_of_duplications(data_frame: pd.DataFrame):
    """
    Calculates duplicated files absence (em3).

    This function gets the dataframe metrics
    and returns the duplicated files absence measure (em3).
    """
    files_duplicated_lines_density = data_frame["duplicated_lines_density"]  # m5 metric

    check_metric_values(files_duplicated_lines_density, "duplicated_lines_density")

    return ems_functions.calculate_em3(data={
        "duplicated_lines_density": files_duplicated_lines_density
    })


def test_coverage(data_frame):
    """
    Calculates test coverage (em6).

    This function gets the dataframe metrics
    and returns the test coverage measure (em6).
    """
    coverage = data_frame["coverage"]  # m6 metric

    check_metric_values(coverage, "coverage")

    return ems_functions.calculate_em6(data={
        "coverage": coverage
    })


def fast_test_builds(data_frame):
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
    })


def passed_tests(data_frame):
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
    })
