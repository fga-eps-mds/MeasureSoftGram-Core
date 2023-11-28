import pytest
from src.core.transformations import diff, norm_diff
from tests.utils.transformations_data import INVALID_DIFF_DATA, VALID_DIFF_DATA
from src.util.exceptions import ReleasePlannedAndDevelopedOfDifferentSizes
import numpy as np

@pytest.mark.parametrize(
    "rp,rd,error_msg",
    INVALID_DIFF_DATA,
)
def test_norm_diff_failure(rp, rd, error_msg):
    rp = np.array(rp)
    rd = np.array(rd)
    with pytest.raises((ReleasePlannedAndDevelopedOfDifferentSizes)) as error:
        norm_diff(rp=rp, rd=rd)
    assert str(error.value) == error_msg


@pytest.mark.parametrize(
    "rp,rd,error_msg",
    INVALID_DIFF_DATA,
)
def test_diff_failure(rp, rd, error_msg):
    rp = np.array(rp)
    rd = np.array(rd)
    with pytest.raises((ReleasePlannedAndDevelopedOfDifferentSizes)) as error:
        diff(rp=rp, rd=rd)
    assert str(error.value) == error_msg


@pytest.mark.parametrize(
    "rp,rd,res",
    VALID_DIFF_DATA,
)
def test_norm_diff_valid(rp, rd, res):
    rp = np.array(rp)
    rd = np.array(rd)
    assert pytest.approx(norm_diff(rp, rd)) == res[0]


@pytest.mark.parametrize(
    "rp,rd,res",
    VALID_DIFF_DATA,
)
def test_diff_valid(rp, rd, res):
    rp = np.array(rp)
    rd = np.array(rd)
    assert pytest.approx(diff(rp, rd)) == res[1]
