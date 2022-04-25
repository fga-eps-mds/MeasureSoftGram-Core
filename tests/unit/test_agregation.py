from src.core.agregation import agregation_operation
from src.core.weighting import weighting_operation
import pytest

WEIGHTS_1 = [0.3333, 0.3333, 0.3333]

WEIGHTS_2 = [0.25, 0.25, 0.50]

VALUES_1 = [0.0010166666666666666, 0.5647222222222222, 0.7142857142857143]

VALUES_2 = [0.67281902, 0.51628390, 0.901926739]


def test_agregation_operation():
    weighted_value_1 = weighting_operation(VALUES_1, WEIGHTS_1)
    weighted_value_2 = weighting_operation(VALUES_2, WEIGHTS_2)
    assert pytest.approx(agregation_operation(weighted_value_1, WEIGHTS_1)) == 0.525711
    assert pytest.approx(agregation_operation(weighted_value_2, WEIGHTS_2)) == 0.813749

    return
