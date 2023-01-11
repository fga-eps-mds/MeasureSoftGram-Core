import pytest
from tests.utils.integration_data import (
    PRE_CONFIGURATION,
    COMPONENT,
    TEST_PARAMETERS,
    CALCULATE_SUBCHARACTERISTICS_SUCCESS_DATA,
    CALCULATE_CHARACTERISTICS_SUCCESS_DATA,
    CALCULATE_SQC_SUCCESS_DATA,
    CALCULATE_ENTITY_INVALID_DATA,
)
from app import app


@pytest.mark.parametrize(
    "status_code,level,expected_output",
    TEST_PARAMETERS
)
def test_analysis_success(status_code, level, expected_output):
    with app.test_client() as client:
        data = {
            "pre_config": PRE_CONFIGURATION,
            "components": COMPONENT,
        }

        response = client.post("/analysis", json=data)

        assert response.status_code == status_code
        assert response.json[level] == expected_output


@pytest.mark.parametrize(
    "data,expected_output",
    CALCULATE_SUBCHARACTERISTICS_SUCCESS_DATA
)
def test_calculate_subcharacteristics_success(data, expected_output):
    with app.test_client() as client:
        response = client.post("/calculate-subcharacteristics/", json=data)

        assert response.status_code == 200
        assert response.json == expected_output


@pytest.mark.parametrize(
    "data,expected_output",
    CALCULATE_CHARACTERISTICS_SUCCESS_DATA,
)
def test_calculate_characteristics_success(data, expected_output):
    with app.test_client() as client:
        response = client.post("/calculate-characteristics/", json=data)

        assert response.status_code == 200
        assert response.json == expected_output


@pytest.mark.parametrize(
    "data,expected_output",
    CALCULATE_SQC_SUCCESS_DATA,
)
def test_calculate_sqc_success(data, expected_output):
    with app.test_client() as client:
        response = client.post("/calculate-sqc/", json=data)

        assert response.status_code == 200
        assert response.json == expected_output


@pytest.mark.parametrize(
    "entity,data",
    CALCULATE_ENTITY_INVALID_DATA,
)
def test_calculate_with_invalid_data(entity, data):
    with app.test_client() as client:
        response = client.post(f"/calculate-{entity}/", json=data)

        assert response.status_code == 422
        assert response.json["error"] == "Failed to validate request"
