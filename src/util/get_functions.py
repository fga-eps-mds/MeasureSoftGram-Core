import numpy as np
import pandas as pd
from exceptions import InvalidGainInterpretationValue
from enum import IntEnum


class GainInterpretation(IntEnum):
    NEGATIVE_SLOPE = -1
    POSITIVE_SLOPE = 1


def create_coordinate_pair(min_threshhold, max_threshold, reverse_y=False):
    """
    Creates a pair of values (x, y), based on the min and max thresholds.
    """
    y = np.array([0, 1]) if reverse_y else np.array([1, 0])

    return np.array([min_threshhold, max_threshold]), y


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


def interpolation(x: np.array, min: float, max: float) -> np.array:
    """
    Interpolates values of x on x_axis[min, max] and y_axis[0, 1]
    """

    y = np.array([0, 1])
    return np.interp(x, np.array([min, max]), y)


def get_files_data_frame(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a data frame with files data.
    """

    return data_frame[
        (data_frame["qualifier"] == "FIL") & (data_frame["ncloc"].astype(float) > 0)
    ]


def get_test_root_dir(data_frame: pd.DataFrame) -> pd.Series:
    """
    Returns a Series populated with "tests" index line from the data_frame.
    """
    dirs = data_frame[data_frame["qualifier"] == "DIR"]

    return dirs.loc[dirs["tests"].astype(float).idxmax()]
