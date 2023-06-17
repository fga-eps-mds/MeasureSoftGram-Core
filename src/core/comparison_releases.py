import numpy as np

from util.exceptions import ReleasePlannedAndDevelopedOfDifferentSizes

"""The normDiff function performs a vector transformation between the planned release vector and the redeveloped release
   vector. This transformation represents the quantitative perception of the difference between the planned quality
   requirement for a release, and the observed result, after its development."""

def normDiff(rp, rd):
    if len(rp) != len(rd):
        raise ReleasePlannedAndDevelopedOfDifferentSizes(
            "The size between planned and developed release vectors is not equal.",
        )
    return np.linalg.norm(rp - rd) / np.linalg.norm(rp)


"""The diff function interprets a vector transformation between the planned and developed release vectors.
    It generates a vector that expresses whether the result observed in a release is above or below the planned quality
    requirement."""

def diff(rp, rd):
    if len(rp) != len(rd):
        raise ReleasePlannedAndDevelopedOfDifferentSizes(
            "The size between planned and developed release vectors is not equal.",
        )
    return [max(0, x - y) for x, y in zip(rp, rd)]