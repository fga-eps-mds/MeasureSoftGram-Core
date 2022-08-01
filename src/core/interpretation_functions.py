import math
import pandas as pd

from src.core.exceptions import InvalidMetricValue, InvalidInterpretationFunctionArguments
from src.core.measures_functions import (
    calculate_em1, calculate_em2, calculate_em3, calculate_em4, calculate_em5, calculate_em6, calculate_em7
)


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


def get_files_data_frame(data_frame):
    """
    Returns a data frame with files data.

    This function returns a data frame with files data.
    """

    return data_frame[
        (data_frame["qualifier"] == "FIL") & (data_frame["ncloc"].astype(float) > 0)
    ]


def get_test_root_dir(data_frame):
    """
    Retorna todas as métricas do diretório de teste
    """

    dirs = data_frame[data_frame["qualifier"] == "DIR"]

    return dirs.loc[dirs["tests"].astype(float).idxmax()]


def non_complex_files_density(data_frame):
    """
    Calculates non-complex files density (em1).

    This function gets the dataframe metrics
    and returns the non-complex files density measure (em1).
    """
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

    return calculate_em1(data={
        "complexity": files_complexity,
        "functions": files_functions,
        "number_of_files": number_of_files,
    })


def commented_files_density(data_frame):
    """
    Calculates commented files density (em2).

    This function gets the dataframe metrics
    and returns the commented files density measure (em2).
    """
    check_arguments(data_frame)
    files_df = get_files_data_frame(data_frame)

    # number_of_files = Tm3 metric
    number_of_files = len(files_df)
    # files_comment_lines_density = m4 metric
    files_comment_lines_density = files_df["comment_lines_density"].astype(float)

    check_number_of_files(number_of_files)
    check_metric_values(files_comment_lines_density, "comment_lines_density")

    return calculate_em2(data={
        "number_of_files": number_of_files,
        "comment_lines_density": files_comment_lines_density,
    })


def absence_of_duplications(data_frame):
    """
    Calculates duplicated files absence (em3).

    This function gets the dataframe metrics
    and returns the duplicated files absence measure (em3).
    """
    check_arguments(data_frame)
    files_df = get_files_data_frame(data_frame)

    # files_duplicated_lines_density = m5 metric
    files_duplicated_lines_density = files_df["duplicated_lines_density"].astype(float)
    # number_of_files = Tm3 metric
    number_of_files = len(files_df)

    check_number_of_files(number_of_files)
    check_metric_values(files_duplicated_lines_density, "duplicated_lines_density")

    return calculate_em3(data={
        "number_of_files": number_of_files,
        "duplicated_lines_density": files_duplicated_lines_density,
    })


def test_coverage(data_frame):
    """
    Calculates test coverage (em6).

    This function gets the dataframe metrics
    and returns the test coverage measure (em6).
    """
    check_arguments(data_frame)
    files_df = get_files_data_frame(data_frame)

    # number_of_files = m3 metric
    number_of_files = len(files_df)
    # test_coverage = m6 metric
    coverage = files_df["coverage"].astype(float)

    check_number_of_files(number_of_files)
    check_metric_values(coverage, "coverage")

    return calculate_em6(data={
        "coverage": coverage,
        "number_of_files": number_of_files,
    })


def fast_test_builds(data_frame):
    """
    Calculates fast test builds (em5)

    This function gets the dataframe metrics
    and returns the fast test builds measure (em5).
    """
    root_test = get_test_root_dir(data_frame)

    check_metric_value(root_test["test_execution_time"], "test_execution_time")

    # test_execution_time = m9 metric
    test_execution_time = float(root_test["test_execution_time"])

    return calculate_em5(data={
        "test_execution_time": test_execution_time
    })


def passed_tests(data_frame):
    """
    Calculates passed tests (em4)

    This function gets the dataframe metrics
    and returns the passed tests measure (em4).
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

    return calculate_em4(data={
        "tests": tests,
        "test_errors": test_errors,
        "test_failures": test_failures,
    })


def ci_feedback_time(data_frame):
    """
    Calculates CI feedback time measure (em7)

    This function calculates average feedback time from CI system.
    """

    root_test = get_test_root_dir(data_frame)

    number_of_build_pipelines_key = next(val for key, val in root_test.iteritems() if key.startswith('number_of_build_pipelines'))
    runtime_sum_of_build_pipelines_key = next(val for key, val in root_test.iteritems() if key.startswith('runtime_sum_of_build_pipelines'))

    check_metric_value(root_test[number_of_build_pipelines_key], "number_of_build_pipelines_in_the_last_x_days")
    check_metric_value(root_test[runtime_sum_of_build_pipelines_key], "runtime_sum_of_build_pipelines_in_the_last_x_days")

    number_of_build_pipelines_in_the_last_x_days = root_test[number_of_build_pipelines_key]
    runtime_sum_of_build_pipelines_in_the_last_x_days = root_test[runtime_sum_of_build_pipelines_key]

    return calculate_em7(data = {
        "number_of_build_pipelines_in_the_last_x_days": number_of_build_pipelines_in_the_last_x_days,
        "runtime_sum_of_build_pipelines_in_the_last_x_days": runtime_sum_of_build_pipelines_in_the_last_x_days
    })
