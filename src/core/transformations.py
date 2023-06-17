import numpy as np
from util.exceptions import InvalidGainInterpretationValue
from enum import IntEnum
from util.check import check_aggregated_weighted_values

class GainInterpretation(IntEnum):
    NEGATIVE_SLOPE = -1
    POSITIVE_SLOPE = 1

def interpretation_function(
    x: np.array,
    min_threshhold: float,
    max_threshold: float,
    gain_interpretation: GainInterpretation,
) -> np.array:
    #  TODO: create docstring in sphinx format

    x = interpolation(x, min_threshhold, max_threshold)

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

def calculate_measure(interpretated_measure: float, number_of_files=None) -> float:
    if number_of_files:
        aggregated_and_normalized_measure = np.divide(
            np.sum(interpretated_measure), number_of_files
        )
        if np.isnan(interpretated_measure) or np.isinf(interpretated_measure):
            return 0
    else:
        aggregated_and_normalized_measure = interpretated_measure
    return aggregated_and_normalized_measure


def calculate_aggregated_weighted_value(values, weights):
    
    check_aggregated_weighted_values(values, weights)
    
    aggregated_weighted_value = np.linalg.norm(np.array(values * weights)) /  np.linalg.norm(weights)
    
    return aggregated_weighted_value