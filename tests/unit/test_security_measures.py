"""
Tests for the security characteristic (US14.01, TASK14.01.01).

The characteristic is structured as ``security`` -> (``confidentiality``,
``integrity``), with two SAST measures from SonarQube, one SAST density measure
and one SCM measure:

- ``security_rating_measure`` and ``security_review_rating_measure`` interpolate
  a 1 (best) to 5 (worst) rating with negative gain, so rating 1 scores 1.00,
  rating 3 scores 0.50 and rating 5 scores 0.00;
- ``absence_of_vulnerabilities`` interpolates vulnerabilities per thousand lines
  of code with negative gain, so a file above ``max_threshold`` scores 0.00;
- ``security_alerts_resolution`` interpolates the percentage of closed alerts
  with positive gain over [45, 100].

Expected values below were calculated by hand from those formulas.
"""

import math

import numpy as np
import pytest

from core.aggregated_normalized_measures import (
    absence_of_vulnerabilities,
    security_alerts_resolution,
    security_rating_measure,
    security_review_rating_measure,
)
from core.measures_functions import (
    NO_ALERTS_RESOLUTION_RATE,
    get_absence_of_vulnerabilities,
    get_security_alerts_resolution,
    get_security_rating,
    get_security_review_rating,
)
from core.schemas import (
    AbsenceOfVulnerabilitiesSchema,
    SecurityAlertsResolutionSchema,
    SecurityRatingSchema,
    SecurityReviewRatingSchema,
)
from marshmallow.exceptions import ValidationError
from resources.analysis import (
    calculate_characteristics,
    calculate_measures,
    calculate_subcharacteristics,
)
from resources.constants import (
    AGGREGATED_NORMALIZED_MEASURES_MAPPING,
    AVAILABLE_PRE_CONFIGS,
)
from staticfiles.default_pre_config import DEFAULT_PRE_CONFIG, SECURITY_PRE_CONFIG
from util.check import Checker
from util.exceptions import ImplicitMetricValueError, InvalidMetricValue
from util.exceptions import InvalidThresholdValue

SECURITY_MEASURES = [
    "security_rating_measure",
    "absence_of_vulnerabilities",
    "security_review_rating_measure",
    "security_alerts_resolution",
]

# Valores esperados da agregacao por media quadratica ponderada com pesos
# iguais, a partir das medidas do teste de ponta a ponta:
# confidentiality = 1.00 (rating A e nenhuma vulnerabilidade)
# integrity = sqrt((0.5^2 + 1.0^2) / 2) (review rating C e alertas resolvidos)
INTEGRITY_VALUE = math.sqrt((0.5**2 + 1.0**2) / 2)
SECURITY_VALUE = math.sqrt((1.0**2 + INTEGRITY_VALUE**2) / 2)


# --------------------------------------------------------------------------
# measures_functions: raw values
# --------------------------------------------------------------------------


def test_get_security_rating_returns_values_and_number_of_files():
    ratings, number_of_files = get_security_rating({"security_rating": [1.0, 3.0]})

    assert list(ratings) == [1.0, 3.0]
    assert number_of_files == 2


def test_get_security_review_rating_returns_values_and_number_of_files():
    ratings, number_of_files = get_security_review_rating(
        {"security_review_rating": [2.0]}
    )

    assert list(ratings) == [2.0]
    assert number_of_files == 1


@pytest.mark.parametrize(
    "get_rating,metric",
    [
        (get_security_rating, "security_rating"),
        (get_security_review_rating, "security_review_rating"),
    ],
)
def test_get_ratings_without_values_returns_zero(get_rating, metric):
    assert get_rating({metric: []}) == 0


@pytest.mark.parametrize(
    "get_rating,metric",
    [
        (get_security_rating, "security_rating"),
        (get_security_review_rating, "security_review_rating"),
    ],
)
def test_get_ratings_rejects_negative_values(get_rating, metric):
    with pytest.raises(InvalidMetricValue) as error:
        get_rating({metric: [-1.0]})

    assert str(error.value) == f'"{metric}" has a value lesser than 0'


def test_get_absence_of_vulnerabilities_returns_density_per_thousand_lines():
    density, number_of_files = get_absence_of_vulnerabilities(
        {"vulnerabilities": [2.0, 1.0], "ncloc": [1000.0, 500.0]}
    )

    assert list(density) == [2.0, 2.0]
    assert number_of_files == 2


def test_get_absence_of_vulnerabilities_without_lines_does_not_divide_by_zero():
    """A file without executable lines cannot host vulnerabilities, so its
    density is 0 instead of a division by zero."""
    density, _ = get_absence_of_vulnerabilities(
        {"vulnerabilities": [0.0], "ncloc": [0.0]}
    )

    assert list(density) == [0.0]
    assert not np.isnan(density).any()
    assert not np.isinf(density).any()


def test_get_absence_of_vulnerabilities_with_metric_lists_of_different_sizes():
    with pytest.raises(ImplicitMetricValueError):
        get_absence_of_vulnerabilities(
            {"vulnerabilities": [1.0], "ncloc": [1000.0, 2000.0]}
        )


def test_get_absence_of_vulnerabilities_without_values_returns_zero():
    assert get_absence_of_vulnerabilities({"vulnerabilities": [], "ncloc": []}) == 0


@pytest.mark.parametrize(
    "metrics,metric",
    [
        ({"vulnerabilities": [-1.0], "ncloc": [1000.0]}, "vulnerabilities"),
        ({"vulnerabilities": [1.0], "ncloc": [-1000.0]}, "ncloc"),
    ],
)
def test_get_absence_of_vulnerabilities_rejects_negative_values(metrics, metric):
    with pytest.raises(InvalidMetricValue) as error:
        get_absence_of_vulnerabilities(metrics)

    assert str(error.value) == f'"{metric}" has a value lesser than 0'


def test_get_security_alerts_resolution_returns_percentage_of_closed_alerts():
    result = get_security_alerts_resolution(
        {"security_alerts_open": 1, "security_alerts_closed": 3}
    )

    assert result == 75.0


def test_get_security_alerts_resolution_without_alerts_scores_full_rate():
    """No alert at all means nothing left to resolve - the best posture, not a
    missing measurement - so the measure must not be punished with 0."""
    result = get_security_alerts_resolution(
        {"security_alerts_open": 0, "security_alerts_closed": 0}
    )

    assert result == NO_ALERTS_RESOLUTION_RATE


def test_get_security_alerts_resolution_rejects_negative_total():
    with pytest.raises(InvalidMetricValue):
        get_security_alerts_resolution(
            {"security_alerts_open": -2, "security_alerts_closed": 1}
        )


# --------------------------------------------------------------------------
# aggregated_normalized_measures: normalization between 0.00 and 1.00
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "aggregated_normalized_measure,data_frame,expected",
    [
        (security_rating_measure, {"security_rating": [1.0]}, 1.0),
        (security_rating_measure, {"security_rating": [3.0]}, 0.5),
        (security_rating_measure, {"security_rating": [5.0]}, 0.0),
        (security_rating_measure, {"security_rating": [1.0, 5.0]}, 0.5),
        (security_review_rating_measure, {"security_review_rating": [1.0]}, 1.0),
        (security_review_rating_measure, {"security_review_rating": [3.0]}, 0.5),
        (security_review_rating_measure, {"security_review_rating": [5.0]}, 0.0),
        (
            absence_of_vulnerabilities,
            {"vulnerabilities": [0.0], "ncloc": [1000.0]},
            1.0,
        ),
        (
            absence_of_vulnerabilities,
            {"vulnerabilities": [0.5], "ncloc": [1000.0]},
            0.5,
        ),
        (
            absence_of_vulnerabilities,
            {"vulnerabilities": [1.0], "ncloc": [1000.0]},
            0.0,
        ),
        (
            security_alerts_resolution,
            {"security_alerts_open": 0.0, "security_alerts_closed": 10.0},
            1.0,
        ),
        (
            security_alerts_resolution,
            {"security_alerts_open": 10.0, "security_alerts_closed": 0.0},
            0.0,
        ),
        (
            security_alerts_resolution,
            {"security_alerts_open": 0.0, "security_alerts_closed": 0.0},
            1.0,
        ),
    ],
)
def test_security_measures_are_normalized_between_zero_and_one(
    aggregated_normalized_measure, data_frame, expected
):
    result = aggregated_normalized_measure(data_frame)

    assert pytest.approx(result) == expected
    assert 0 <= result <= 1.0


def test_absence_of_vulnerabilities_above_max_threshold_scores_zero():
    """Files whose density is above max_threshold are out of the interpretation
    window and must not pull the measure above 0."""
    result = absence_of_vulnerabilities(
        {"vulnerabilities": [50.0], "ncloc": [1000.0]},
    )

    assert result == 0.0


@pytest.mark.parametrize(
    "aggregated_normalized_measure,data_frame",
    [
        (security_rating_measure, {"security_rating": []}),
        (security_review_rating_measure, {"security_review_rating": []}),
        (absence_of_vulnerabilities, {"vulnerabilities": [], "ncloc": []}),
    ],
)
def test_security_measures_without_metrics_return_zero(
    aggregated_normalized_measure, data_frame
):
    assert aggregated_normalized_measure(data_frame) == 0.0


@pytest.mark.parametrize(
    "aggregated_normalized_measure,data_frame,error_msg",
    [
        (
            security_rating_measure,
            {"security_rating": [None]},
            '"security_rating" has an invalid metric value',
        ),
        (
            security_review_rating_measure,
            {"security_review_rating": ["abc"]},
            '"security_review_rating" has an invalid metric value',
        ),
        (
            absence_of_vulnerabilities,
            {"vulnerabilities": [None], "ncloc": [1000.0]},
            '"vulnerabilities" has an invalid metric value',
        ),
        (
            absence_of_vulnerabilities,
            {"vulnerabilities": [1.0], "ncloc": [None]},
            '"ncloc" has an invalid metric value',
        ),
    ],
)
def test_security_measures_with_invalid_metrics(
    aggregated_normalized_measure, data_frame, error_msg
):
    with pytest.raises(InvalidMetricValue) as error:
        aggregated_normalized_measure(data_frame)

    assert str(error.value) == error_msg


# --------------------------------------------------------------------------
# check: reference values
# --------------------------------------------------------------------------


@pytest.mark.parametrize("measure", SECURITY_MEASURES)
def test_security_measures_have_a_threshold_check(measure):
    """Checker.check_threshold resolves the check by measure name, so a missing
    one would break the calculation with InvalidCheckThreshold."""
    assert hasattr(Checker, f"check_{measure}_threshold")


@pytest.mark.parametrize(
    "measure,min_threshold,max_threshold",
    [
        ("security_rating_measure", 1, 5),
        ("security_rating_measure", 1, 3),
        ("security_review_rating_measure", 2, 5),
        ("absence_of_vulnerabilities", 0, 1),
        ("absence_of_vulnerabilities", 0, 10),
        ("security_alerts_resolution", 45, 100),
        ("security_alerts_resolution", 0, 80),
    ],
)
def test_security_thresholds_accept_adjusted_reference_values(
    measure, min_threshold, max_threshold
):
    """The reference values are editable in the "Modificar valores de
    referencia" step, so the check validates a range and not an exact value."""
    Checker.check_threshold(min_threshold, max_threshold, measure)


@pytest.mark.parametrize(
    "measure,min_threshold,max_threshold,error_msg",
    [
        (
            "security_rating_measure",
            0,
            5,
            "min_threshold is lesser than 1",
        ),
        (
            "security_rating_measure",
            1,
            6,
            "max_threshold is greater than 5",
        ),
        (
            "security_review_rating_measure",
            4,
            2,
            "min_threshold is greater or equal to max_threshold",
        ),
        (
            "absence_of_vulnerabilities",
            -1,
            1,
            "min_threshold is lesser than 0",
        ),
        (
            "absence_of_vulnerabilities",
            1,
            1,
            "min_threshold is greater or equal to max_threshold",
        ),
        (
            "security_alerts_resolution",
            -1,
            100,
            "min_threshold is lesser than 0",
        ),
        (
            "security_alerts_resolution",
            80,
            80,
            "min_threshold is greater or equal to max_threshold",
        ),
        (
            "security_alerts_resolution",
            45,
            101,
            "max_threshold is greater than 100",
        ),
    ],
)
def test_security_thresholds_reject_invalid_reference_values(
    measure, min_threshold, max_threshold, error_msg
):
    with pytest.raises(InvalidThresholdValue) as error:
        Checker.check_threshold(min_threshold, max_threshold, measure)

    assert str(error.value) == error_msg


# --------------------------------------------------------------------------
# schemas
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "schema,metrics",
    [
        (SecurityRatingSchema, [{"key": "security_rating", "value": [1.0]}]),
        (
            SecurityReviewRatingSchema,
            [{"key": "security_review_rating", "value": [1.0]}],
        ),
        (
            AbsenceOfVulnerabilitiesSchema,
            [
                {"key": "vulnerabilities", "value": [2.0]},
                {"key": "ncloc", "value": [1000.0]},
            ],
        ),
        (
            SecurityAlertsResolutionSchema,
            [
                {"key": "security_alerts_open", "value": [1.0]},
                {"key": "security_alerts_closed", "value": [3.0]},
            ],
        ),
    ],
)
def test_security_schemas_accept_their_own_metrics(schema, metrics):
    schema().load({"metrics": metrics})
    schema().validate_metrics(metrics)


@pytest.mark.parametrize(
    "schema",
    [
        SecurityRatingSchema,
        SecurityReviewRatingSchema,
        AbsenceOfVulnerabilitiesSchema,
        SecurityAlertsResolutionSchema,
    ],
)
def test_security_schemas_reject_foreign_metrics(schema):
    metrics = [{"key": "coverage", "value": [80.0]}]

    with pytest.raises(ValidationError) as error:
        schema.validate_metrics(metrics)

    assert "Métrica não presente na medida" in str(error.value)


@pytest.mark.parametrize(
    "value,error_msg",
    [
        ([1.0, 2.0], "array de um único valor"),
        ([1], "valor flutuante"),
    ],
)
def test_security_alerts_resolution_schema_requires_a_single_float(value, error_msg):
    metrics = [{"key": "security_alerts_open", "value": value}]

    with pytest.raises(ValidationError) as error:
        SecurityAlertsResolutionSchema.validate_metrics(metrics)

    assert error_msg in str(error.value)


# --------------------------------------------------------------------------
# configuration catalog and end to end aggregation
# --------------------------------------------------------------------------


def test_security_is_available_in_the_pre_config_catalog():
    characteristic = AVAILABLE_PRE_CONFIGS["characteristics"]["security"]

    assert characteristic["subcharacteristics"] == ["confidentiality", "integrity"]

    for subcharacteristic in characteristic["subcharacteristics"]:
        assert AVAILABLE_PRE_CONFIGS["subcharacteristics"][subcharacteristic][
            "characteristics"
        ] == ["security"]


@pytest.mark.parametrize("measure", SECURITY_MEASURES)
def test_security_measures_are_mapped_to_a_function_and_a_schema(measure):
    assert measure in AGGREGATED_NORMALIZED_MEASURES_MAPPING
    assert measure in AVAILABLE_PRE_CONFIGS["measures"]


def test_default_pre_config_stays_without_security():
    """Products planned without security keep only the three configured
    characteristics - security is opt in."""
    keys = [c["key"] for c in DEFAULT_PRE_CONFIG["characteristics"]]

    assert "security" not in keys


def test_security_pre_config_weights_sum_100_at_every_level():
    characteristic = SECURITY_PRE_CONFIG["characteristics"][0]

    assert characteristic["key"] == "security"
    assert sum(s["weight"] for s in characteristic["subcharacteristics"]) == 100

    for subcharacteristic in characteristic["subcharacteristics"]:
        assert sum(m["weight"] for m in subcharacteristic["measures"]) == 100


def test_security_pre_config_declares_reference_values_for_every_measure():
    measures = [
        measure
        for subcharacteristic in SECURITY_PRE_CONFIG["characteristics"][0][
            "subcharacteristics"
        ]
        for measure in subcharacteristic["measures"]
    ]

    assert sorted(m["key"] for m in measures) == sorted(SECURITY_MEASURES)

    for measure in measures:
        assert measure["min_threshold"] < measure["max_threshold"]


def test_security_characteristic_is_calculated_from_metrics_to_characteristic():
    """Walks the whole pipeline with the security config: metrics -> measures ->
    subcharacteristics -> characteristic."""
    extracted_measures = {
        "measures": [
            {
                "key": "security_rating_measure",
                "metrics": [
                    {"key": "security_rating", "value": [1.0]},
                ],
            },
            {
                "key": "absence_of_vulnerabilities",
                "metrics": [
                    {"key": "vulnerabilities", "value": [0.0]},
                    {"key": "ncloc", "value": [1000.0]},
                ],
            },
            {
                "key": "security_review_rating_measure",
                "metrics": [
                    {"key": "security_review_rating", "value": [3.0]},
                ],
            },
            {
                "key": "security_alerts_resolution",
                "metrics": [
                    {"key": "security_alerts_open", "value": [0.0]},
                    {"key": "security_alerts_closed", "value": [10.0]},
                ],
            },
        ]
    }

    calculated = calculate_measures(extracted_measures, SECURITY_PRE_CONFIG)
    values = {m["key"]: m["value"] for m in calculated["measures"]}

    assert pytest.approx(values["security_rating_measure"]) == 1.0
    assert pytest.approx(values["absence_of_vulnerabilities"]) == 1.0
    assert pytest.approx(values["security_review_rating_measure"]) == 0.5
    assert pytest.approx(values["security_alerts_resolution"]) == 1.0

    subcharacteristic_config = SECURITY_PRE_CONFIG["characteristics"][0][
        "subcharacteristics"
    ]
    extracted_subcharacteristics = {
        "subcharacteristics": [
            {
                "key": subcharacteristic["key"],
                "measures": [
                    {
                        "key": measure["key"],
                        "value": values[measure["key"]],
                        "weight": measure["weight"],
                    }
                    for measure in subcharacteristic["measures"]
                ],
            }
            for subcharacteristic in subcharacteristic_config
        ]
    }

    calculated_subcharacteristics = calculate_subcharacteristics(
        extracted_subcharacteristics
    )
    subcharacteristic_values = {
        s["key"]: s["value"]
        for s in calculated_subcharacteristics["subcharacteristics"]
    }

    # calculate_aggregated_weighted_value agrega por media quadratica
    # ponderada (norma euclidiana), nao por media aritmetica: com pesos iguais,
    # integrity = sqrt((0.5^2 + 1.0^2) / 2).
    assert pytest.approx(subcharacteristic_values["confidentiality"]) == 1.0
    assert pytest.approx(subcharacteristic_values["integrity"]) == INTEGRITY_VALUE

    extracted_characteristics = {
        "characteristics": [
            {
                "key": "security",
                "subcharacteristics": [
                    {
                        "key": subcharacteristic["key"],
                        "value": subcharacteristic_values[subcharacteristic["key"]],
                        "weight": subcharacteristic["weight"],
                    }
                    for subcharacteristic in subcharacteristic_config
                ],
            }
        ]
    }

    calculated_characteristics = calculate_characteristics(extracted_characteristics)
    security = calculated_characteristics["characteristics"][0]

    assert security["key"] == "security"
    assert pytest.approx(security["value"]) == SECURITY_VALUE
    assert 0 <= security["value"] <= 1.0
