from enum import IntEnum

import numpy as np

from util.check import Checker
from util.exceptions import InvalidGainInterpretationValue


class GainInterpretation(IntEnum):
    NEGATIVE_SLOPE = -1
    POSITIVE_SLOPE = 1


def interpretation_function(
    x: np.array,
    min_threshold: float,
    max_threshold: float,
    gain_interpretation: GainInterpretation,
) -> np.array:
    #  TODO: create docstring in sphinx format

    x = interpolation(x, min_threshold, max_threshold)

    if gain_interpretation == GainInterpretation.POSITIVE_SLOPE:
        return x
    elif gain_interpretation == GainInterpretation.NEGATIVE_SLOPE:
        return 1 - x
    else:
        InvalidGainInterpretationValue(
            f"Gain Interpretation need be 1 or -1, but received {gain_interpretation}"
        )


def interpolation(x: np.array, min: float, max: float) -> np.array:
    """
    Interpolates values of x on x_axis[min, max] and y_axis[0, 1]
    """

    y = np.array([0, 1])
    return np.interp(x, np.array([min, max]), y)


def calculate_measure(interpretated_measure: np.array, number_of_files=None) -> float:
    if number_of_files:
        print(f"input {interpretated_measure}")
        print(f"soma {np.sum(interpretated_measure)}")
        print(f"number of files {number_of_files}")
        print(f"division {np.divide(np.sum(interpretated_measure), number_of_files)}")
        aggregated_and_normalized_measure = np.divide(
            np.sum(interpretated_measure), number_of_files
        )
        print(
            np.isnan(interpretated_measure).all(), np.isinf(interpretated_measure).all()
        )
        if (
            np.isnan(interpretated_measure).all()
            or np.isinf(interpretated_measure).all()
        ):
            return 0
    else:
        aggregated_and_normalized_measure = interpretated_measure
    return aggregated_and_normalized_measure


def calculate_aggregated_weighted_value(values, weights):
    Checker.check_aggregated_weighted_values(values, weights)

    aggregated_weighted_value = np.linalg.norm(
        np.array(values * weights)
    ) / np.linalg.norm(weights)

    return aggregated_weighted_value
