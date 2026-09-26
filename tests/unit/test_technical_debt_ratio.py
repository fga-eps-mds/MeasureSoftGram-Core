"""
Tests for the technical_debt_ratio measure (issue #7 of 2026.2-MeasureSoftGram-Service).

The measure follows the same logic as absence_of_duplications: each file's
``sqale_debt_ratio`` is interpolated on [min_threshold, max_threshold] with a
negative gain, files above max_threshold score 0, and the result is the mean
over all files. Expected values below were calculated by hand with
score = 1 - ratio / 20 for the default thresholds (0, 20).
"""

import numpy as np
import pytest

from core.aggregated_normalized_measures import technical_debt_ratio
from core.measures_functions import get_technical_debt_ratio
from resources.analysis import (
    calculate_characteristics,
    calculate_measures,
    calculate_subcharacteristics,
    calculate_tsqmi,
)
from resources.constants import AVAILABLE_PRE_CONFIGS
from staticfiles.default_pre_config import DEFAULT_PRE_CONFIG
from util.exceptions import InvalidMetricValue

MODIFIABILITY_MEASURES = [
    "non_complex_file_density",
    "commented_file_density",
    "duplication_absense",
    "technical_debt_ratio",
]


def _modifiability_config():
    for characteristic in DEFAULT_PRE_CONFIG["characteristics"]:
        for subcharacteristic in characteristic["subcharacteristics"]:
            if subcharacteristic["key"] == "modifiability":
                return characteristic, subcharacteristic
    raise AssertionError("modifiability not found in DEFAULT_PRE_CONFIG")


def _extracted_measures(values):
    return {
        "measures": [
            {
                "key": "technical_debt_ratio",
                "metrics": [{"key": "sqale_debt_ratio", "value": values}],
            }
        ]
    }


@pytest.mark.parametrize(
    "sqale_debt_ratio,expected",
    [
        ([0.0, 0.0], 1.0),
        ([20.0, 20.0], 0.0),
        ([20.1, 50.0, 300.0], 0.0),
        ([10.0, 10.0], 0.5),
        ([5.0, 5.0], 0.75),
        ([2.5, 7.5], 0.75),
        ([0.0, 5.0, 10.0, 20.0, 40.0], 0.45),
    ],
)
def test_technical_debt_ratio_hand_calculated_values(sqale_debt_ratio, expected):
    result = technical_debt_ratio({"sqale_debt_ratio": sqale_debt_ratio})

    assert result == pytest.approx(expected)


def test_technical_debt_ratio_higher_debt_means_lower_score():
    ratios = np.arange(0.0, 25.0, 2.5)
    scores = [technical_debt_ratio({"sqale_debt_ratio": [r, r]}) for r in ratios]

    assert all(a > b for a, b in zip(scores, scores[1:]) if a > 0)
    assert scores[0] == 1.0
    assert scores[-1] == 0.0


def test_get_technical_debt_ratio_returns_values_and_number_of_files():
    values, number_of_files = get_technical_debt_ratio(
        {"sqale_debt_ratio": [1.0, 2.0, 3.0]}
    )

    assert list(values) == [1.0, 2.0, 3.0]
    assert number_of_files == 3


def test_get_technical_debt_ratio_without_files_returns_zero():
    assert get_technical_debt_ratio({"sqale_debt_ratio": []}) == 0


def test_get_technical_debt_ratio_negative_values_raise():
    with pytest.raises(InvalidMetricValue, match="lesser than 0"):
        get_technical_debt_ratio({"sqale_debt_ratio": [-5.0, 1.0]})


def test_calculate_measures_uses_default_thresholds_from_pre_config():
    result = calculate_measures(
        extracted_measures=_extracted_measures([5.0, 5.0]),
        config=DEFAULT_PRE_CONFIG,
    )

    assert result["measures"] == [
        {"key": "technical_debt_ratio", "value": pytest.approx(0.75)}
    ]


def test_calculate_measures_uses_thresholds_from_config():
    config = {
        "characteristics": [
            {
                "subcharacteristics": [
                    {
                        "measures": [
                            {
                                "key": "technical_debt_ratio",
                                "min_threshold": 0,
                                "max_threshold": 10,
                            }
                        ]
                    }
                ]
            }
        ]
    }

    result = calculate_measures(
        extracted_measures=_extracted_measures([5.0, 5.0]), config=config
    )

    assert result["measures"][0]["value"] == pytest.approx(0.5)


def test_calculate_measures_without_sqale_debt_ratio_raises():
    extracted = {"measures": [{"key": "technical_debt_ratio", "metrics": []}]}

    with pytest.raises(InvalidMetricValue, match="sqale_debt_ratio"):
        calculate_measures(extracted_measures=extracted)


def test_technical_debt_ratio_belongs_to_modifiability_and_maintainability():
    measure = AVAILABLE_PRE_CONFIGS["measures"]["technical_debt_ratio"]

    assert measure["subcharacteristics"] == ["modifiability"]
    assert measure["characteristics"] == ["maintainability"]
    assert measure["metrics"] == ["sqale_debt_ratio"]
    assert "technical_debt_ratio" in (
        AVAILABLE_PRE_CONFIGS["subcharacteristics"]["modifiability"]["measures"]
    )
    assert "modifiability" in (
        AVAILABLE_PRE_CONFIGS["characteristics"]["maintainability"][
            "subcharacteristics"
        ]
    )


def test_default_pre_config_modifiability_has_four_measures_with_25_percent():
    characteristic, modifiability = _modifiability_config()
    weights = {m["key"]: m["weight"] for m in modifiability["measures"]}

    assert characteristic["key"] == "maintainability"
    assert list(weights) == MODIFIABILITY_MEASURES
    assert set(weights.values()) == {25}
    assert sum(weights.values()) == 100


def test_default_pre_config_technical_debt_ratio_thresholds():
    _, modifiability = _modifiability_config()
    measure = next(
        m for m in modifiability["measures"] if m["key"] == "technical_debt_ratio"
    )

    assert measure["min_threshold"] == 0
    assert measure["max_threshold"] == 20


def _tsqmi_for_technical_debt_ratio(value, weights=(25, 25, 25, 25)):
    measures = [
        {"key": key, "value": 1.0, "weight": weight}
        for key, weight in zip(MODIFIABILITY_MEASURES, weights)
    ]
    measures[-1]["value"] = value

    modifiability = calculate_subcharacteristics(
        {"subcharacteristics": [{"key": "modifiability", "measures": measures}]}
    )["subcharacteristics"][0]["value"]

    maintainability = calculate_characteristics(
        {
            "characteristics": [
                {
                    "key": "maintainability",
                    "subcharacteristics": [
                        {"key": "modifiability", "value": modifiability, "weight": 100}
                    ],
                }
            ]
        }
    )["characteristics"][0]["value"]

    tsqmi = calculate_tsqmi(
        {
            "tsqmi": {
                "key": "tsqmi",
                "characteristics": [
                    {"key": "maintainability", "value": maintainability, "weight": 100}
                ],
            }
        }
    )["tsqmi"][0]["value"]

    return modifiability, maintainability, tsqmi


def test_technical_debt_ratio_is_aggregated_up_to_tsqmi():
    best = _tsqmi_for_technical_debt_ratio(1.0)
    worst = _tsqmi_for_technical_debt_ratio(0.0)

    assert best == pytest.approx((1.0, 1.0, 1.0))
    # ||(25, 25, 25, 0)|| / ||(25, 25, 25, 25)|| = sqrt(3 / 4)
    assert worst == pytest.approx((np.sqrt(0.75),) * 3)


def test_technical_debt_ratio_custom_weight_changes_aggregation():
    _, _, default_weights = _tsqmi_for_technical_debt_ratio(0.0)
    _, _, heavier_weight = _tsqmi_for_technical_debt_ratio(
        0.0, weights=(20, 20, 20, 40)
    )

    # ||(20, 20, 20, 0)|| / ||(20, 20, 20, 40)|| = sqrt(1200 / 2800)
    assert heavier_weight == pytest.approx(np.sqrt(1200 / 2800))
    assert heavier_weight < default_weights
