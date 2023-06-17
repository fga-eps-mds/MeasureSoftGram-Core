import json

from src.parsers.sonarqube import Sonarqube


def test_extract_sonarqube_available_metrics():
    with open("tests/unit/data/to_extract.msgram", "r") as f:
        metrics = json.loads(f.read())
    extracted_metrics = Sonarqube().extract_supported_metrics(metrics)

    with open("tests/unit/data/extracted.msgram", "r") as f:
        assert set(extracted_metrics.keys()).issubset(json.loads(f.read()).keys())
