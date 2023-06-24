from enum import IntEnum

import numpy as np

from util.check import Checker
from util.exceptions import (
    InvalidGainInterpretationValue,
    ReleasePlannedAndDevelopedOfDifferentSizes,
)


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
        aggregated_and_normalized_measure = np.divide(
            np.sum(interpretated_measure), number_of_files
        )
        if np.isnan(aggregated_and_normalized_measure) or np.isinf(
            aggregated_and_normalized_measure
        ):
            return 0.0
    else:
        aggregated_and_normalized_measure = interpretated_measure
    return aggregated_and_normalized_measure


def calculate_aggregated_weighted_value(values, weights):
    Checker.check_aggregated_weighted_values(values, weights)

    aggregated_weighted_value = np.linalg.norm(
        np.array(values * weights)
    ) / np.linalg.norm(weights)

    return aggregated_weighted_value


def norm_diff(rp, rd):
    """The norm_diff function performs a vector transformation between the planned release vector and the redeveloped
    release vector. This transformation represents the quantitative perception of the difference between the
    planned quality requirement for a release, and the observed result, after its development.
    """

    if len(rp) != len(rd):
        raise ReleasePlannedAndDevelopedOfDifferentSizes(
            "The size between planned and developed release vectors is not equal.",
        )
    return np.linalg.norm(rp - rd) / np.linalg.norm(rp)


def diff(rp, rd):
    """The diff function interprets a vector transformation between the planned and developed release vectors.
    It generates a vector that expresses whether the result observed in a release is above or below the planned quality
    requirement."""
    if len(rp) != len(rd):
        raise ReleasePlannedAndDevelopedOfDifferentSizes(
            "The size between planned and developed release vectors is not equal.",
        )
    return [max(0, x - y) for x, y in zip(rp, rd)]
