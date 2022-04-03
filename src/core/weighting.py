import numpy as np


def weighting_operation(df, weights):
    df = np.array(df)
    weights = np.array(weights)
    return df * weights
