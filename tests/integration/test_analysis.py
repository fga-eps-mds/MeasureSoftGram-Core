from tests.test_helpers import read_json
import json
from src.app import app

PRE_CONFIGURATION = {
    "_id": "6265b525ab15bc00c4effbd0",
    "name": "pre-config-test-analysis",
    "characteristics": {
        "reliability": {
            "expected_value": 70,
            "weight": 50,
            "subcharacteristics": ["testing_status"],
            "weights": {"testing_status": 100},
        },
        "maintainability": {
            "expected_value": 30,
            "weight": 50,
            "subcharacteristics": ["modifiability"],
            "weights": {"modifiability": 100},
        },
    },
    "subcharacteristics": {
        "testing_status": {
            "weights": {"passed_tests": 100},
            "measures": ["passed_tests"],
        },
        "modifiability": {
            "weights": {"non_complex_file_density": 100},
            "measures": ["non_complex_file_density"],
        },
    },
    "measures": ["passed_tests", "non_complex_file_density"],
}

JSON_FILE = read_json(
    "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-Service-04-12-2022-17-32-35-v1.1.0.json"
)

COMPONENT = {
    "pre_config_id": "6265b525ab15bc00c4effbd0",
    "components": JSON_FILE["components"],
    "language_extension": "py",
}


def test_analysis_sucess():
    with app.test_client() as client:

        data = {
            "pre_config": PRE_CONFIGURATION,
            "components": COMPONENT,
        }

        response = client.post("/analysis", json=data)

        assert response.status_code == 200
        assert response.json == {
            "characteristics": {
                "maintainability": 0.5,
                "reliability": 0.7142857142857143,
            },
            "sqc": {"sqc": 0.6165241607725739},
            "subcharacteristics": {
                "modifiability": 0.5,
                "testing_status": 0.7142857142857143,
            },
        }
