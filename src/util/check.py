import math

import numpy as np

from util.exceptions import (
    InvalidCheckThreshold,
    InvalidMetricValue,
    InvalidThresholdValue,
    ValuesAndWeightsOfDifferentSizes,
)


class Checker:
    @staticmethod
    def check_non_complex_files_density_threshold(
        min_complex_files_density: float, max_complex_files_density: float
    ):
        if min_complex_files_density != 0:
            raise InvalidThresholdValue("min_complex_files_density is not equal to 0")

        if min_complex_files_density >= max_complex_files_density:
            raise InvalidThresholdValue(
                "min_complex_files_density is greater or equal to max_complex_files_density"
            )

    @staticmethod
    def check_comment_files_density_threshold(
        min_comment_density: float, max_comment_density: float
    ):
        if min_comment_density < 0:
            raise InvalidThresholdValue("min_comment_density is lesser than 0")
        if min_comment_density >= max_comment_density:
            raise InvalidThresholdValue(
                "min_comment_density is greater or equal to max_comment_density"
            )
        if max_comment_density > 100:
            raise InvalidThresholdValue("max_comment_density is greater than 100")

    @staticmethod
    def check_absence_of_duplications_threshold(
        min_duplicated_lines: float, max_duplicated_lines: float
    ):
        if min_duplicated_lines != 0:
            raise InvalidThresholdValue("min_duplicated_lines is not equal to 0")

        if min_duplicated_lines >= max_duplicated_lines:
            raise InvalidThresholdValue(
                "min_duplicated_lines is greater or equal to max_duplicated_lines"
            )

        if max_duplicated_lines > 100:
            raise InvalidThresholdValue("max_duplicated_lines is greater than 100")

    @staticmethod
    def check_test_coverage_threshold(min_coverage, max_coverage):
        if min_coverage < 0:
            raise InvalidThresholdValue("min_coverage is lesser than 0")

        if min_coverage >= max_coverage:
            raise InvalidThresholdValue(
                "min_coverage is greater or equal to max_coverage"
            )

        if max_coverage != 100:
            raise InvalidThresholdValue("max_coverage is not equal to 100")

    @staticmethod
    def check_fast_test_builds_threshold(
        min_fast_test_time: float, max_fast_test_time: float
    ):
        if min_fast_test_time != 0:
            raise InvalidThresholdValue(("min_fast_test_time is not equal to 0"))

        if min_fast_test_time >= max_fast_test_time:
            raise InvalidThresholdValue(
                "min_fast_test_time is greater or equal to max_fast_test_time"
            )

    @staticmethod
    def check_passed_tests_threshold(min_passed_tests: float, max_passed_tests: float):
        if min_passed_tests != 0:
            raise InvalidThresholdValue("min_passed_tests is not equal to 0")

        if max_passed_tests != 1:
            raise InvalidThresholdValue("max_passed_tests is not equal to 1")

    @staticmethod
    def check_threshold(min: float, max: float, measure: str):
        check_function = getattr(Checker, f"check_{measure}_threshold", None)
        if check_function is None:
            raise InvalidCheckThreshold("Check function not implemented")
        check_function(min, max)

    @staticmethod
    def check_metric_value(metric_value, metric):
        try:
            if metric_value is None or math.isnan(float(metric_value)):
                raise InvalidMetricValue(f'"{metric}" has an invalid metric value')
        except (ValueError, TypeError):
            raise InvalidMetricValue(f'"{metric}" has an invalid metric value')

    @staticmethod
    def check_metric_values(metric_values, metric):
        if not isinstance(metric_values, (list, np.ndarray)):
            raise InvalidMetricValue(f'"{metric}" is not a list or a np.ndarray')

        # if not len(metric_values):
        #     raise InvalidMetricValue(f'"{metric}" is empty')

        for value in metric_values:
            Checker.check_metric_value(value, metric)

    @staticmethod
    def check_aggregated_weighted_values(values, weights):
        if len(values) != len(weights):
            raise ValuesAndWeightsOfDifferentSizes(
                "The length of weight and values are not equal",
            )
