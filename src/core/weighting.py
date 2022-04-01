import numpy as np
from src.core.exceptions import InvalidWeightSize


def weighting_operation(df, weights):
    if len(df) == len(weights):
        df = np.array(df)
        weights = np.array(weights)
        return df * weights
    else:
        raise InvalidWeightSize
