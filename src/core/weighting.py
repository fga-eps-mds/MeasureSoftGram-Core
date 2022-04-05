import numpy as np

from src.core.exceptions import InvalidEqualityOfWeightAndValues


def weighting_operation(values, weights):
    if len(values) != len(weights):
        raise InvalidEqualityOfWeightAndValues
    else:
        values = np.array(values)
        weights = np.array(weights)
        return values * weights
