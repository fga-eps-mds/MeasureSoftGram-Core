from core.analysis import calculate_measures
from core.analysis import resolve_level
from core.analysis import make_analysis

from tests.utils.analysis_data import (
    CALCULATE_MEASURES_DATA,
    RESOLVE_LEVEL_DATA,
    MAKE_ANALYSIS_DATA,
)

import pytest


@pytest.mark.parametrize(
    "measure,data_frame,expected_value",
    CALCULATE_MEASURES_DATA,
)
def test_calculate_measures(measure, data_frame, expected_value):
    calculation_result = calculate_measures(data_frame, [measure])
    assert (
        pytest.approx(calculation_result[measure]) == expected_value
    )


@pytest.mark.parametrize(
    "subs,measures,type,expected",
    RESOLVE_LEVEL_DATA,
)
def test_resolve_level(subs, measures, type, expected):
    aggregate_level, _ = resolve_level(subs, measures, type)
    assert pytest.approx(aggregate_level["testing_status"]) == expected


@pytest.mark.parametrize(
    "measures,subs,characteristics,expected,key_value",
    MAKE_ANALYSIS_DATA,
)
def test_make_analysis(
    measures,
    subs,
    characteristics,
    expected,
    key_value
):
    sqc, agregated_sbc, aggregated_characteristics, _, _, _ = make_analysis(
        measures, subs, characteristics
    )
    assert pytest.approx(agregated_sbc[key_value[0]]) == expected[0]
    assert pytest.approx(aggregated_characteristics[key_value[1]]) == expected[1]
    assert pytest.approx(sqc[key_value[2]]) == expected[2]
