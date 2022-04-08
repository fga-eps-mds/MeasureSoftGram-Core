import numpy as np

from src.core.exceptions import InvalidEqualityOfWeightAndValues


def weighting_operation(values, weights):
    if len(values) != len(weights):
        raise InvalidEqualityOfWeightAndValues["The length of weight and values are not equal"]    
    
    values = np.array(values)
    weights = np.array(weights)
    
    return values * weights
