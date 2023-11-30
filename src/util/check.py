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
        min_threshold: float, max_threshold: float
    ):
        if min_threshold != 0:
            raise InvalidThresholdValue("min_threshold is not equal to 0")

        if min_threshold >= max_threshold:
            raise InvalidThresholdValue(
                "min_threshold is greater or equal to max_threshold"
            )

    @staticmethod
    def check_comment_files_density_threshold(
        min_threshold: float, max_threshold: float
    ):
        if min_threshold < 0:
            raise InvalidThresholdValue("min_threshold is lesser than 0")
        if min_threshold >= max_threshold:
            raise InvalidThresholdValue(
                "min_threshold is greater or equal to max_threshold"
            )
        if max_threshold > 100:
            raise InvalidThresholdValue("max_threshold is greater than 100")

    @staticmethod
    def check_absence_of_duplications_threshold(
        min_threshold: float, max_threshold: float
    ):
        if min_threshold != 0:
            raise InvalidThresholdValue("min_threshold is not equal to 0")

        if min_threshold >= max_threshold:
            raise InvalidThresholdValue(
                "min_threshold is greater or equal to max_threshold"
            )

        if max_threshold > 100:
            raise InvalidThresholdValue("max_threshold is greater than 100")

    @staticmethod
    def check_test_coverage_threshold(min_threshold, max_threshold):
        if min_threshold < 0:
            raise InvalidThresholdValue("min_threshold is lesser than 0")

        if min_threshold >= max_threshold:
            raise InvalidThresholdValue(
                "min_threshold is greater or equal to max_threshold"
            )

        if max_threshold != 100:
            raise InvalidThresholdValue("max_threshold is not equal to 100")

    @staticmethod
    def check_fast_test_builds_threshold(min_threshold: float, max_threshold: float):
        if min_threshold != 0:
            raise InvalidThresholdValue(("min_threshold is not equal to 0"))

        if min_threshold >= max_threshold:
            raise InvalidThresholdValue(
                "min_threshold is greater or equal to max_threshold"
            )

    @staticmethod
    def check_passed_tests_threshold(min_threshold: float, max_threshold: float):
        if min_threshold != 0:
            raise InvalidThresholdValue("min_threshold is not equal to 0")

        if max_threshold != 1:
            raise InvalidThresholdValue("max_threshold is not equal to 1")

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

    @staticmethod
    def check_team_throughput_threshold(min_threshold: float, max_threshold: float):
        if min_threshold != 45:
            raise InvalidThresholdValue("min_threshold is not equal to 45")

        if max_threshold != 100:
            raise InvalidThresholdValue("max_threshold is not equal to 100")
