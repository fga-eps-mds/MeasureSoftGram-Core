import pytest
from marshmallow.exceptions import ValidationError

from resources.analysis import (
    calculate_characteristics,
    calculate_measures,
    calculate_subcharacteristics,
    calculate_tsqmi,
)
from tests.utils.analysis_data import (
    CALCULATE_CHARACTERISTICS_ERROR_INFOS,
    CALCULATE_CHARACTERISTICS_RESULT_DATA,
    CALCULATE_MEASURES_ERROR_INFOS,
    CALCULATE_MEASURES_RESULT_DATA,
    CALCULATE_RUNTIME_MEASURES_RESULT_DATA,
    CALCULATE_SUBCHARACTERISTICS_ERROR_INFOS,
    CALCULATE_SUBCHARACTERISTICS_RESULT_DATA,
    CALCULATE_TSQMI_ERROR_INFOS,
    CALCULATE_TSQMI_RESULT_DATA,
    EXTRACTED_CHARACTERISTICS_DATA,
    EXTRACTED_MEASURES_DATA,
    EXTRACTED_RUNTIME_MEASURES_DATA,
    EXTRACTED_SUBCHARACTERISTICS_DATA,
    EXTRACTED_TSQMI_DATA,
)
from util.exceptions import MeasureKeyNotSupported


def test_calculate_measures_success():
    calculation_result = calculate_measures(extracted_measures=EXTRACTED_MEASURES_DATA)
    assert "measures" in calculation_result

    measures_result = calculation_result.get("measures")
    measures_expected = CALCULATE_MEASURES_RESULT_DATA.get("measures")
    for measure_result, measure_expected in zip(measures_result, measures_expected):
        assert measure_result.get("key") == measure_expected.get("key")
        assert pytest.approx(measure_result.get("value")) == measure_expected.get(
            "value"
        )


def test_calculate_runtime_measures_success():
    calculation_result = calculate_measures(
        extracted_measures=EXTRACTED_RUNTIME_MEASURES_DATA
    )
    assert "measures" in calculation_result

    measures_result = calculation_result.get("measures")
    measures_expected = CALCULATE_RUNTIME_MEASURES_RESULT_DATA.get("measures")
    for measure_result, measure_expected in zip(measures_result, measures_expected):
        assert measure_result.get("key") == measure_expected.get("key")
        assert measure_result.get("value") == pytest.approx(
            measure_expected.get("value")
        )


@pytest.mark.parametrize(
    "extracted_measures_data, error_msg",
    CALCULATE_MEASURES_ERROR_INFOS,
)
def test_calculate_measures_errors(extracted_measures_data, error_msg):
    with pytest.raises((ValidationError, MeasureKeyNotSupported)) as error:
        calculate_measures(extracted_measures=extracted_measures_data)
    assert error_msg in str(error.value)


def test_calculate_subcharacteristics_sucess():
    calculation_result = calculate_subcharacteristics(
        extracted_subcharacteristics=EXTRACTED_SUBCHARACTERISTICS_DATA
    )
    assert "subcharacteristics" in calculation_result

    subcharacteristics_result = calculation_result.get("subcharacteristics")
    subcharacteristics_expected = CALCULATE_SUBCHARACTERISTICS_RESULT_DATA.get(
        "subcharacteristics"
    )
    for subcharacteristic_result, subcharacteristic_expected in zip(
        subcharacteristics_result, subcharacteristics_expected
    ):
        assert subcharacteristic_result.get("key") == subcharacteristic_expected.get(
            "key"
        )
        assert pytest.approx(
            subcharacteristic_result.get("value")
        ) == subcharacteristic_expected.get("value")


@pytest.mark.parametrize(
    "extracted_subcharacteristcs_data,error_msg",
    CALCULATE_SUBCHARACTERISTICS_ERROR_INFOS,
)
def test_calcula_subcharacteristics_errors(extracted_subcharacteristcs_data, error_msg):
    with pytest.raises((ValidationError, MeasureKeyNotSupported)) as error:
        calculate_subcharacteristics(
            extracted_subcharacteristics=extracted_subcharacteristcs_data
        )
    assert str(error.value) == error_msg


def test_calculate_characteristics_success():
    calculation_result = calculate_characteristics(
        extracted_characteristics=EXTRACTED_CHARACTERISTICS_DATA
    )
    assert "characteristics" in calculation_result

    characteristics_result = calculation_result.get("characteristics")
    characteristics_expected = CALCULATE_CHARACTERISTICS_RESULT_DATA.get(
        "characteristics"
    )
    for characteristic_result, characteristic_expected in zip(
        characteristics_result, characteristics_expected
    ):
        assert characteristic_result.get("key") == characteristic_expected.get("key")
        assert pytest.approx(
            characteristic_result.get("value")
        ) == characteristic_expected.get("value")


@pytest.mark.parametrize(
    "extracted_characteristics_data,error_msg",
    CALCULATE_CHARACTERISTICS_ERROR_INFOS,
)
def test_calcula_characteristics_errors(extracted_characteristics_data, error_msg):
    with pytest.raises((ValidationError, MeasureKeyNotSupported)) as error:
        calculate_characteristics(
            extracted_characteristics=extracted_characteristics_data
        )
    assert str(error.value) == error_msg


def test_calculate_tsqmi_success():
    calculation_result = calculate_tsqmi(extracted_tsqmi=EXTRACTED_TSQMI_DATA)
    assert "tsqmi" in calculation_result

    tsqmi_result = calculation_result.get("tsqmi")
    tsqmi_expected = CALCULATE_TSQMI_RESULT_DATA.get("tsqmi")
    for tsqmi_result, tsqmi_expected in zip(tsqmi_result, tsqmi_expected):
        assert tsqmi_result.get("key") == tsqmi_expected.get("key")
        assert pytest.approx(tsqmi_result.get("value")) == tsqmi_expected.get("value")


@pytest.mark.parametrize(
    "extracted_tsqmi_data,error_msg",
    CALCULATE_TSQMI_ERROR_INFOS,
)
def test_calcula_tsqmi_errors(extracted_tsqmi_data, error_msg):
    with pytest.raises((ValidationError, MeasureKeyNotSupported)) as error:
        calculate_tsqmi(extracted_tsqmi=extracted_tsqmi_data)
    assert str(error.value) == error_msg


@pytest.mark.parametrize(
    "measure_key,metrics,expected",
    [
        ("technical_debt_ratio", {"sqale_debt_ratio": [8.3]}, 0.585),
        ("test_coverage", {"coverage": [85.0]}, 0.625),
        ("commented_file_density", {"comment_lines_density": [20.0]}, 0.5),
        ("duplication_absense", {"duplicated_lines_density": [0.0]}, 1.0),
        ("non_complex_file_density", {"complexity": [4.0], "functions": [2.0]}, 0.8),
        (
            "passed_tests",
            {"tests": [10.0], "test_errors": [1.0], "test_failures": [1.0]},
            0.8,
        ),
        ("test_builds", {"test_execution_time": [600.0], "tests": [10.0]}, 0.9998),
    ],
)
def test_calculate_measures_single_file(measure_key, metrics, expected):
    extracted_measures = {
        "measures": [
            {
                "key": measure_key,
                "metrics": [
                    {"key": key, "value": value} for key, value in metrics.items()
                ],
            }
        ]
    }
    result = calculate_measures(extracted_measures=extracted_measures)
    assert result["measures"][0]["key"] == measure_key
    assert pytest.approx(result["measures"][0]["value"]) == expected
