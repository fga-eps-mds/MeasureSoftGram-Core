import pytest

from core.transformations import calculate_aggregated_weighted_value
from tests.utils.aggregation_data import VALUES_1, VALUES_2, WEIGHTS_1, WEIGHTS_2


def test_aggregation_operation():
    assert (
        pytest.approx(calculate_aggregated_weighted_value(VALUES_1, WEIGHTS_1))
        == 0.525711
    )
    assert (
        pytest.approx(calculate_aggregated_weighted_value(VALUES_2, WEIGHTS_2))
        == 0.813749
    )
