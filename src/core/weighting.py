import numpy as np

from util.exceptions import ValuesAndWeightsOfDifferentSizes


def weighting_operation(values, weights):
    if len(values) != len(weights):
        raise ValuesAndWeightsOfDifferentSizes(
            "The length of weight and values are not equal",
        )

    values = np.array(values)
    weights = np.array(weights)

    return values * weights
