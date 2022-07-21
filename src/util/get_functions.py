import numpy as np
import pandas as pd


def create_coordinate_pair(min_threshhold, max_threshold, reverse_y=False):
    """
    Creates a pair of values (x, y), based on the min and max thresholds.
    """
    y = np.array([0, 1]) if reverse_y else np.array([1, 0])

    return np.array([min_threshhold, max_threshold]), y


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
