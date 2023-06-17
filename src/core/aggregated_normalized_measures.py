import numpy as np

import core.measures_functions as ems_functions
from core.transformations import calculate_measure, interpretation_function
from util.check import Checker


def non_complex_files_density(
    data_frame,
    min_complex_files_density: float = 0,
    max_complex_files_density: float = 10,
):
    """
    Calculates non-complex files density.
    This function calculates non-complex files density measure
    used to assess the changeability quality subcharacteristic.

    This function gets the dataframe metrics
    and returns the non-complex files density measure.
    """
    files_complexity = np.array(data_frame["complexity"])
    files_functions = np.array(data_frame["functions"])

    Checker.check_metric_values(files_complexity, "complexity")
    Checker.check_metric_values(files_functions, "functions")

    Checker.check_threshold(
        min_complex_files_density,
        max_complex_files_density,
        "non_complex_files_density",
    )

    (
        complex_files_density,
        number_of_files,
    ) = ems_functions.get_non_complex_files_density(
        data={
            "complexity": files_complexity,
            "functions": files_functions,
        }
    )

    files_in_thresholds_bool_index = complex_files_density <= max_complex_files_density
    files_functions_gt_zero_bool_index = files_functions > 0
    x = complex_files_density[
        files_in_thresholds_bool_index * files_functions_gt_zero_bool_index
    ]

    interpretation_function_value = interpretation_function(
        x=x,
        min_threshold=min_complex_files_density,
        max_threshold=max_complex_files_density,
        gain_interpretation=-1,
    )

    aggregated_and_normalized_measure = calculate_measure(
        interpretation_function_value, number_of_files
    )
    return aggregated_and_normalized_measure


def commented_files_density(
    data_frame, min_comment_density: float = 10, max_comment_density: float = 30
):
    """
    Calculates commented files density.

    This function gets the dataframe metrics
    and returns the commented files density measure.
    """
    files_comment_lines_density = data_frame["comment_lines_density"]

    Checker.check_metric_values(files_comment_lines_density, "comment_lines_density")

    Checker.check_threshold(
        min_comment_density, max_comment_density, "comment_files_density"
    )

    (
        files_comment_lines_density,
        number_of_files,
    ) = ems_functions.get_commented_files_density(
        data={
            "comment_lines_density": files_comment_lines_density,
        }
    )

    x = files_comment_lines_density[
        files_comment_lines_density.between(
            min_comment_density,
            max_comment_density,
            inclusive="both",
        )
    ]
    interpretation_function_value = interpretation_function(
        x=x,
        min_threshold=min_comment_density,
        max_threshold=max_comment_density,
        gain_interpretation=-1,
    )
    aggregated_and_normalized_measure = calculate_measure(
        interpretation_function_value, number_of_files
    )
    return aggregated_and_normalized_measure


def absence_of_duplications(
    data_frame, min_duplicated_lines: float = 0, max_duplicated_lines: float = 5.0
):
    """
    Calculates duplicated files absence (em3).

    This function gets the dataframe metrics
    and returns the duplicated files absence measure (em3).
    """
    files_duplicated_lines_density = data_frame["duplicated_lines_density"]  # m5 metric

    Checker.check_metric_values(
        files_duplicated_lines_density, "duplicated_lines_density"
    )

    Checker.check_threshold(
        min_duplicated_lines, max_duplicated_lines, "absence_of_duplications"
    )

    (
        files_duplicated_lines_density,
        number_of_files,
    ) = ems_functions.get_absence_of_duplications(
        data={"duplicated_lines_density": files_duplicated_lines_density},
    )

    x = files_duplicated_lines_density[
        files_duplicated_lines_density <= max_duplicated_lines
    ]

    interpretation_function_value = interpretation_function(
        x=x,
        min_threshold=min_duplicated_lines,
        max_threshold=max_duplicated_lines,
        gain_interpretation=-1,
    )
    aggregated_and_normalized_measure = calculate_measure(
        interpretation_function_value, number_of_files
    )
    return aggregated_and_normalized_measure


def test_coverage(
    data_frame,
    min_coverage: float = 60,
    max_coverage: float = 100,
):
    """
    Calculates test coverage (em6).

    This function gets the dataframe metrics
    and returns the test coverage measure (em6).
    """
    coverage = data_frame["coverage"]  # m6 metric

    Checker.check_metric_values(coverage, "coverage")

    Checker.check_threshold(min_coverage, max_coverage, "test_coverage")

    coverage, number_of_files = ems_functions.get_test_coverage(
        data={"coverage": coverage},
    )
    x = coverage[coverage >= min_coverage]
    interpretation_function_value = interpretation_function(
        x=x,
        min_threshold=min_coverage,
        max_threshold=max_coverage,
        gain_interpretation=1,
    )
    aggregated_and_normalized_measure = calculate_measure(
        interpretation_function_value, number_of_files
    )
    return aggregated_and_normalized_measure


def fast_test_builds(
    data_frame, min_fast_test_time: float = 0, max_fast_test_time: float = 300000
):
    """
    Calculates fast test builds (em5)
    This function gets the dataframe metrics
    and returns the fast test builds measure (em5).
    """
    test_execution_time = data_frame["test_execution_time"]
    tests = data_frame["tests"]

    Checker.check_metric_values(test_execution_time, "test_execution_time")
    Checker.check_metric_values(tests, "tests")

    Checker.check_threshold(min_fast_test_time, max_fast_test_time, "fast_test_builds")

    (
        execution_time,
        number_of_files,
        number_of_tests,
    ) = ems_functions.get_fast_test_builds(
        data={"test_execution_time": test_execution_time, "tests": tests},
    )

    # Apply threshold
    execution_between_thresholds = execution_time[execution_time <= max_fast_test_time]
    x = np.divide(execution_between_thresholds, number_of_tests)

    interpretation_function_value = interpretation_function(
        x=x / 100,  # ask to teacher
        min_threshold=min_fast_test_time,
        max_threshold=max_fast_test_time,
        gain_interpretation=-1,
    )

    aggregated_and_normalized_measure = calculate_measure(
        interpretation_function_value, number_of_files
    )

    return aggregated_and_normalized_measure


def passed_tests(data_frame, min_passed_tests: float = 0, max_passed_tests: float = 1):
    """
    Calculates passed tests (em4)

    This function gets the dataframe metrics
    and returns the passed tests measure (em4).
    """

    tests = data_frame["tests"]  # m6 metrics
    test_errors = data_frame["test_errors"]  # m7 metrics
    test_failures = data_frame["test_failures"]  # m8 metrics

    Checker.check_metric_values(tests, "tests")
    Checker.check_metric_value(test_failures, "test_failures")
    Checker.check_metric_value(test_errors, "test_errors")

    Checker.check_threshold(min_passed_tests, max_passed_tests, "passed_tests")

    number_of_tests, number_of_fail_tests = ems_functions.get_passed_tests(
        data={
            "tests": tests,
            "test_errors": float(test_errors),
            "test_failures": float(test_failures),
        }
    )

    x = np.divide((number_of_tests - number_of_fail_tests), number_of_tests)

    interpretation_function_value = interpretation_function(
        x=x,
        min_threshold=min_passed_tests,
        max_threshold=max_passed_tests,
        gain_interpretation=1,
    )

    aggregated_and_normalized_measure = calculate_measure(interpretation_function_value)

    return aggregated_and_normalized_measure
