import numpy as np


def aggregation_operation(weighted_value, weights):
    weighted_value = np.array(weighted_value)
    weights = np.array(weights)
    normalized_value = np.linalg.norm(weighted_value)
    max_value = np.linalg.norm(weights)
    return normalized_value / max_value
