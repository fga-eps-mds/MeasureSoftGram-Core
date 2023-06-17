from resources.analysis import (
    calculate_measures,
    calculate_subcharacteristics,
    calculate_characteristics,
    calculate_tsqmi
)
from tests.utils.analysis_data import (
    EXTRACTED_MEASURES_DATA, CALCULATE_MEASURES_RESPONSE_DATA,
    CALCULATE_MEASURES_ERROR_INFOS, EXTRACTED_SUBCHARACTERISTICS_DATA,
    CALCULATE_SUBCHARACTERISTICS_RESPONSE_DATA, CALCULATE_SUBCHARACTERISTICS_ERROR_INFOS,
    EXTRACTED_CHARACTERISTICS_DATA, CALCULATE_CHARACTERISTICS_RESPONSE_DATA,
    CALCULATE_CHARACTERISTICS_ERROR_INFOS, EXTRACTED_TSQMI_DATA,
    CALCULATE_TSQMI_RESPONSE_DATA, CALCULATE_TSQMI_ERROR_INFOS,
)

import pytest


def test_calculate_measures_success():
    calculation_result = calculate_measures(extracted_measures=EXTRACTED_MEASURES_DATA)
    assert calculation_result == CALCULATE_MEASURES_RESPONSE_DATA


@pytest.mark.parametrize(
    "extracted_measure_data,error_msg",
    CALCULATE_MEASURES_ERROR_INFOS,
)
def test_calcula_measures_errors(extracted_measure_data, error_msg):
    error_response = calculate_measures(extracted_measures=extracted_measure_data)
    assert error_response['error'] == error_msg
    assert error_response['code'] == 422


def test_calculate_subcharacteristics_sucess():
    calculation_result = calculate_subcharacteristics(extracted_subcharacteristics=EXTRACTED_SUBCHARACTERISTICS_DATA)
    assert calculation_result == CALCULATE_SUBCHARACTERISTICS_RESPONSE_DATA


@pytest.mark.parametrize(
    "extracted_subcharacteristcs_data,error_msg",
    CALCULATE_SUBCHARACTERISTICS_ERROR_INFOS,
)
def test_calcula_subcharacteristics_errors(extracted_subcharacteristcs_data, error_msg):
    error_response = calculate_subcharacteristics(extracted_subcharacteristics=extracted_subcharacteristcs_data)
    assert error_response['error'] == error_msg
    assert error_response['code'] == 422


def test_calculate_characteristics_success():
    calculation_result = calculate_characteristics(extracted_characteristics=EXTRACTED_CHARACTERISTICS_DATA)
    assert calculation_result == CALCULATE_CHARACTERISTICS_RESPONSE_DATA


@pytest.mark.parametrize(
    "extracted_characteristics_data,error_msg",
    CALCULATE_CHARACTERISTICS_ERROR_INFOS,
)
def test_calcula_characteristics_errors(extracted_characteristics_data, error_msg):
    error_response = calculate_characteristics(extracted_characteristics=extracted_characteristics_data)
    assert error_response['error'] == error_msg
    assert error_response['code'] == 422


def test_calculate_tsqmi_success():
    calculation_result = calculate_tsqmi(extracted_tsqmi=EXTRACTED_TSQMI_DATA)
    assert calculation_result == CALCULATE_TSQMI_RESPONSE_DATA


@pytest.mark.parametrize(
    "extracted_tsqmi_data,error_msg",
    CALCULATE_TSQMI_ERROR_INFOS,
)
def test_calcula_tsqmi_errors(extracted_tsqmi_data, error_msg):
    error_response = calculate_tsqmi(extracted_tsqmi=extracted_tsqmi_data)
    assert error_response['error'] == error_msg
    assert error_response['code'] == 422
