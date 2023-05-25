from typing import Dict

import numpy as np
import pandas as pd

from util.exceptions import (
    ImplicitMetricValueError,
    InvalidMetricValue,
    InvalidThresholdValue,
)
from util.get_functions import create_coordinate_pair


def interpolate_series(series, x, y):
    """
    Interpolates a series using the given x and y values.

    This function interpolates a series using the given x and y values.
    """

    return [np.interp(item / 100, x, y) for item in series]


def resolve_metric_list_parameter(metric):
    """
    Resolves the metric list parameter to calculate a measure

    This functions converts the metric parameter to a pandas Series if it is a list (CalculateMeasures endpoint)
    otherwise it just returns the metric - already a pandas Series (Analysis endpoint).
    """
    return pd.Series(metric, dtype=np.float64) if isinstance(metric, list) else metric


def calculate_em1(
    data: Dict,
    min_complex_files_density: float = 0,
    max_complex_files_density: float = 10,
):
    """
    Calculates non-complex files density (em1).

    This function calculates non-complex files density measure (em1)
    used to assess the changeability quality sub characteristic.
    """
    if min_complex_files_density != 0:
        raise InvalidThresholdValue(("min_complex_files_density is not equal to 0"))

    if min_complex_files_density >= max_complex_files_density:
        raise InvalidThresholdValue(
            (
                "min_complex_files_density is greater or equal to"
                " max_complex_files_density"
            )
        )

    # if max_complex_files_density > 100:
    #     raise InvalidThresholdValue(("max_complex_files_density is greater than 100"))

    files_complexity = resolve_metric_list_parameter(data["complexity"])
    files_functions = resolve_metric_list_parameter(data["functions"])

    if "number_of_files" in data:
        number_of_files = data["number_of_files"]

    elif len(files_complexity) != len(files_functions):
        raise ImplicitMetricValueError(
            (
                "Unable to get the implicit value of metric `number_of_file` "
                "because the size of the lists of values of metrics `complexity` "
                "and `functions` are not equal."
            )
        )
    else:
        number_of_files = len(files_complexity)

    has_none = files_complexity is None or files_functions is None
    has_zero = len(files_complexity) == 0 or len(files_functions) == 0

    if has_none or has_zero:
        return 0

    if files_complexity.sum() <= 0:
        raise InvalidMetricValue(
            "The cyclomatic complexity of all files is lesser or equal than 0"
        )

    if files_functions.sum() <= 0:
        raise InvalidMetricValue(
            "The number of functions of all files is lesser or equal than 0"
        )

    x, y = create_coordinate_pair(
        min_complex_files_density,
        max_complex_files_density,
    )

    files_in_thresholds_df = files_complexity / files_functions
    files_in_thresholds_bool_index = files_in_thresholds_df <= max_complex_files_density
    files_functions_gt_zero_bool_index = files_functions > 0
    IF1 = np.interp(
        list(
            files_in_thresholds_df[
                files_in_thresholds_bool_index * files_functions_gt_zero_bool_index
            ]
        ),
        x,
        y,
    )
    em1 = np.divide(sum(IF1), number_of_files)

    if np.isnan(em1) or np.isinf(em1):
        return 0
    return em1


def calculate_em2(
    data: Dict,
    min_comment_density: float = 10,
    max_comment_density: float = 30,
):
    """
    Calculates commented files density (em2).

    This function calculates commented files density measure (em2)
    used to assess the changeability quality sub characteristic.
    """
    if min_comment_density < 0:
        raise InvalidThresholdValue(("min_comment_density is lesser than 0"))

    if min_comment_density >= max_comment_density:
        raise InvalidThresholdValue(
            ("min_comment_density is greater or equal to" " max_comment_density")
        )
    if max_comment_density > 100:
        raise InvalidThresholdValue(("max_comment_density is greater than 100"))

    files_comment_lines_density = resolve_metric_list_parameter(
        data["comment_lines_density"]
    )

    if "number_of_files" in data:
        number_of_files = data["number_of_files"]
    else:
        number_of_files = len(files_comment_lines_density)

    has_none = files_comment_lines_density is None
    has_zero = len(files_comment_lines_density) == 0

    if has_none or has_zero:
        return 0

    if files_comment_lines_density.sum() < 0:
        raise InvalidMetricValue(
            "The number of files comment lines density is lesser than 0"
        )

    x, y = create_coordinate_pair(
        min_comment_density / 100,
        max_comment_density / 100,
    )

    files_between_thresholds = files_comment_lines_density[
        files_comment_lines_density.between(
            min_comment_density,
            max_comment_density,
            inclusive="both",
        )
    ]

    em2i = interpolate_series(files_between_thresholds, x, y)
    em2 = np.divide(np.sum(em2i), number_of_files)

    if np.isnan(em2) or np.isinf(em2):
        return 0
    return em2


def calculate_em3(
    data: Dict,
    min_duplicated_lines: float = 0,
    max_duplicated_lines: float = 5.0,
):
    """
    Calculates duplicated files absence (em3).

    This function calculates the duplicated files absence measure (em3)
    used to assess the changeability quality sub characteristic.
    """
    if min_duplicated_lines != 0:
        raise InvalidThresholdValue(("min_duplicated_lines is not equal to 0"))

    if min_duplicated_lines >= max_duplicated_lines:
        raise InvalidThresholdValue(
            ("min_duplicated_lines is greater or equal to" " max_duplicated_lines")
        )

    if max_duplicated_lines > 100:
        raise InvalidThresholdValue(("max_duplicated_lines is greater than 100"))

    files_duplicated_lines_density = resolve_metric_list_parameter(
        data["duplicated_lines_density"]
    )

    if "number_of_files" in data:
        number_of_files = data["number_of_files"]
    else:
        number_of_files = len(files_duplicated_lines_density)

    has_none = files_duplicated_lines_density is None
    has_zero = len(files_duplicated_lines_density) == 0

    if has_none or has_zero:
        return 0

    if files_duplicated_lines_density.sum() < 0:
        raise InvalidMetricValue(
            "The number of files duplicated lines density is lesser than 0"
        )

    x, y = create_coordinate_pair(
        min_duplicated_lines / 100,
        max_duplicated_lines / 100,
    )

    files_below_threshold = files_duplicated_lines_density[
        files_duplicated_lines_density <= max_duplicated_lines
    ]

    em3i = interpolate_series(files_below_threshold, x, y)
    em3 = np.divide(np.sum(em3i), number_of_files)

    if np.isnan(em3) or np.isinf(em3):
        return 0
    return em3


def calculate_em4(
    data: Dict[str, float],
    min_passed_tests: float = 0,
    max_passed_tests: float = 1,
):
    """
    Calculates passed tests (em4)

    This function calculates the passed tests measure (em4)
    used to assess the testing status sub characteristic.
    """
    if min_passed_tests != 0:
        raise InvalidThresholdValue(("min_passed_tests is not equal to 0"))

    if max_passed_tests != 1:
        raise InvalidThresholdValue(("max_passed_tests is not equal to 1"))
    try:
        # number_of_tests está retornando valores incorretos
        number_of_tests = resolve_metric_list_parameter(data["tests"]).sum()
        number_of_test_errors = data["test_errors"]
        number_of_test_failures = data["test_failures"]

        x, y = create_coordinate_pair(
            min_passed_tests,
            max_passed_tests,
            reverse_y=True,
        )

        number_of_fail_tests = number_of_test_errors + number_of_test_failures
        if4i = np.divide((number_of_tests - number_of_fail_tests), number_of_tests)

    except ZeroDivisionError:
        return 0

    else:
        if np.isnan(if4i) or np.isinf(if4i):
            return 0
        return np.interp(if4i, x, y)


def calculate_em5(
    data: Dict[str, list],
    min_fast_test_time: float = 0,
    max_fast_test_time: float = 300000,
):
    """
    Calculates fast test builds (em5)

    This function calculates the fast test builds measure (em5)
    used to assess the testing status sub characteristic.
    """
    if min_fast_test_time != 0:
        raise InvalidThresholdValue(("min_fast_test_time is not equal to 0"))

    if min_fast_test_time >= max_fast_test_time:
        raise InvalidThresholdValue(
            ("min_fast_test_time is greater or equal to" " max_fast_test_time")
        )

    execution_time = resolve_metric_list_parameter(data["test_execution_time"])
    number_of_tests = resolve_metric_list_parameter(data["tests"])
    number_of_files = len(execution_time)

    has_none = execution_time is None or number_of_tests is None
    has_zero = len(execution_time) == 0 or len(number_of_tests) == 0

    if has_none or has_zero:
        return 0

    x, y = create_coordinate_pair(min_fast_test_time, max_fast_test_time)

    execution_between_thresholds = execution_time[execution_time <= max_fast_test_time]
    fast_tests_between_thresholds = np.divide(
        execution_between_thresholds, number_of_tests
    )

    em5i = interpolate_series(fast_tests_between_thresholds, x, y)
    em5 = np.divide(np.sum(em5i), number_of_files)

    if np.isnan(em5) or np.isinf(em5):
        return 0

    return em5


def calculate_em6(
    data: Dict,
    min_coverage: float = 60,
    max_coverage: float = 90,
):
    """
    Calculates test coverage (em6).

    This function calculates the test coverage measure (em6)
    used to assess the testing status sub characteristic.
    """
    if min_coverage < 0:
        raise InvalidThresholdValue(("min_coverage is lesser than 0"))

    if min_coverage >= max_coverage:
        raise InvalidThresholdValue(
            ("min_coverage is greater or equal to" " max_coverage")
        )

    if max_coverage > 100:
        raise InvalidThresholdValue(("max_coverage is greater than 100"))

    coverage = resolve_metric_list_parameter(data["coverage"])

    if "number_of_files" in data:
        number_of_files = data["number_of_files"]
    else:
        number_of_files = len(coverage)

    has_none = coverage is None
    has_zero = len(coverage) == 0

    if has_none or has_zero:
        return 0

    x, y = create_coordinate_pair(
        min_coverage / 100,
        max_coverage / 100,
        reverse_y=True,
    )

    files_between_thresholds = coverage[coverage >= min_coverage]
    em6i = interpolate_series(files_between_thresholds, x, y)
    em6 = np.divide(np.sum(em6i), number_of_files)

    if np.isnan(em6) or np.isinf(em6):
        return 0
    return em6


def calculate_em7(data: Dict):
    """
    Calculates team throughput (em7).

    This function calculates the team throughput measure (em7)
    used to assess the functional completeness subcharacteristic.
    """
    resolved_issues_with_us_label = data[
        "number_of_resolved_issues_with_US_label_in_the_last_x_days"
    ]

    total_issues_with_us_label = data[
        "total_number_of_issues_with_US_label_in_the_last_x_days"
    ]

    x, y = create_coordinate_pair(0, 1, reverse_y=True)

    if7 = np.divide(resolved_issues_with_us_label, total_issues_with_us_label)

    if np.isnan(if7) or np.isinf(if7):
        return 0
    return np.interp(if7, x, y)
