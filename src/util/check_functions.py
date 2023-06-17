import math

# import pandas as pd

from util.exceptions import (
    # InvalidInterpretationFunctionArguments,
    InvalidMetricValue,
)


# NOTE: Esses métodos eram utilizados na função do dataframe
#       que era utilizado nas funções de interpretação,
#       porém foi retirado devido ao empacotamento.
#       Assim, estão comentadas caso venham a ser utilizadas novamente.
# def check_component_is_valid(component, language_extension):

#     return (
#         component["qualifier"] == "DIR" or component["language"] == language_extension
#     )


# def check_arguments(data_frame: pd.DataFrame):
#     """
#     Raises an InvalidInterpretationFunctionArguments exception if argument it's not a pandas.DataFrame.
#     """

#     if not isinstance(data_frame, pd.DataFrame):
#         raise InvalidInterpretationFunctionArguments(
#             "Expected data_frame to be a pandas.DataFrame"
#         )


# def check_number_of_files(number_of_files):
#     """
#     Raises an InvalidMetricValue exception if the number of files is lesser or equal than 0.
#     """

#     if number_of_files <= 0:
#         raise InvalidMetricValue("The number of files is lesser or equal than 0")


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


def check_thresholds(min, max, measure):
    callable(f"check_{measure}")(min, max)


def check_non_complex_files_density(
    min_complex_files_density, max_complex_files_density
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
