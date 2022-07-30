import pytest
from tests.utils.integration_data import (
    PRE_CONFIGURATION,
    COMPONENT,
    TEST_PARAMETERS,
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
