import numpy as np


def agregation_operation(weighted_value, weigths):
    weighted_value = np.array(weighted_value)
    weigths = np.array(weigths)
    normalized_value = np.linalg.norm(weighted_value)
    max_value = np.linalg.norm(weigths)
    return normalized_value / max_value
