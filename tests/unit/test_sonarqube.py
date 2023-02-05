import json
import pytest
from requests import Response

from unittest.mock import patch

from src.parsers.sonarqube import Sonarqube


@pytest.mark.parametrize(
    "status_code",
    [200, 400]
)
def test_get_request_in_sonarqube(status_code):
    response = Response()
    response.status_code = status_code
    response._content = json.dumps({}).encode('utf-8')

    with patch("requests.get", return_value=response) as mock_data:
        Sonarqube().extract_supported_metrics([])

    mock_data.assert_called()


def test_extract_sonarqube_available_metrics():
    with open('tests/unit/data/to_extract.msgram', 'r') as f:
        metrics = json.loads(f.read())
    extracted_metrics = Sonarqube().extract_supported_metrics(metrics)

    with open('tests/unit/data/extracted.msgram', 'r') as f:
        assert set(extracted_metrics.keys()).issubset(json.loads(f.read()).keys())
