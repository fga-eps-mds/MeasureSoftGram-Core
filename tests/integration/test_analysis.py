import pytest
from tests.utils.integration_data import (
    PRE_CONFIGURATION,
    COMPONENT,
    TEST_PARAMETERS,
    CALCULATE_SUBCHARACTERISTICS_DATA,
)
from src.app import app


@pytest.mark.parametrize(
    "status_code,level,expected_output",
    TEST_PARAMETERS
)
def test_analysis_sucess(status_code, level, expected_output):
    with app.test_client() as client:
        data = {
            "pre_config": PRE_CONFIGURATION,
            "components": COMPONENT,
        }

        response = client.post("/analysis", json=data)

        assert response.status_code == status_code
        assert response.json[level] == expected_output


@pytest.mark.parametrize(
    "data,status_code,expected_output",
    CALCULATE_SUBCHARACTERISTICS_DATA
)
def test_calculate_subcharacteristics(data, status_code, expected_output):
    with app.test_client() as client:
        response = client.post("/calculate-subcharacteristics/", json=data)

        assert response.status_code == status_code
        assert response.json == expected_output
