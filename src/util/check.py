import math

from util.exceptions import (
    InvalidMetricValue,
    InvalidThresholdValue,
    InvalidCheckThreshold,
    ValuesAndWeightsOfDifferentSizes
)


def check_metric_value(metric_value, metric):
    try:
        if metric_value is None or math.isnan(float(metric_value)):
            raise InvalidMetricValue(f'"{metric}" has an invalid metric value')
    except (ValueError, TypeError):
        raise InvalidMetricValue(f'"{metric}" has an invalid metric value')


def check_metric_values(metric_values, metric):
    if not isinstance(metric_values, list):
        raise InvalidMetricValue(f'"{metric}" is not a list')

    if not len(metric_values):
        raise InvalidMetricValue(f'"{metric}" is empty')

    for value in metric_values:
        check_metric_value(value, metric)



def check_non_complex_files_density_threshold(
    min_complex_files_density: float, 
    max_complex_files_density: float
):
    if min_complex_files_density != 0:
        raise InvalidThresholdValue(("min_complex_files_density is not equal to 0"))

    if min_complex_files_density >= max_complex_files_density:
        raise InvalidThresholdValue(
            (
                "min_complex_files_density is greater or equal to"
                " max_complex_files_density"
            )
        )


threshold_check_mapping = {
    "check_non_complex_files_density": check_non_complex_files_density_threshold
}


def check_threshold(min: float, max: float, measure: str):
    threshold_check_mapping.get(f"check_{measure}_threshold", InvalidCheckThreshold("Check function not implemented"))(min, max)



def check_aggregated_weighted_values(values, weights):
    if len(values) != len(weights):
        raise ValuesAndWeightsOfDifferentSizes(
            "The length of weight and values are not equal",
        )
