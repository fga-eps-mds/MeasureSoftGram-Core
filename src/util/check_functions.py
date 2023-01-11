import math

import pandas as pd

from util.exceptions import (
    InvalidInterpretationFunctionArguments,
    InvalidMetricValue,
)


def check_component_is_valid(component, language_extension):

    return (
        component["qualifier"] == "DIR" or component["language"] == language_extension
    )


def check_arguments(data_frame: pd.DataFrame):
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
