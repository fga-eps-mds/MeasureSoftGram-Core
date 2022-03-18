""" AVAILABLE_PRE_CONFIGS = {
    "reliability": {
        "name": "Reliability",
        "subcharacteristics": {
            "testing_status": {
                "name": "Testing Status",
                "measures": {
                    "passed_tests": {"name": "Passed Tests"},
                    "test_builds": {"name": "Test Builds"},
                    "test_coverage": {"name": "Test Coverage"},
                },
            }
        },
    },
    "maintainability": {
        "name": "Maintainability",
        "subcharacteristics": {
            "modifiability": {
                "name": "Modifiability",
                "measures": {
                    "non_complex_file_density": {"name": "Non complex file density"},
                    "commented_file_density": {"name": "Commented file density"},
                    "duplication_absense": {"name": "Duplication abscense"},
                },
            }
        },
    },
} """

AVAILABLE_PRE_CONFIGS = {
    "characteristics": {
        "reliability": {
            "name": "Reliability",
            "subcharacteristics": ["testing_status"],
        },
        "maintainability": {
            "name": "Maintainability",
            "subcharacteristics": ["modifiability"],
        },
    },
    "subcharacteristics": {
        "testing_status": {
            "name": "Testing Status",
            "measures": ["passed_tests", "test_builds", "test_coverage"],
            "characteristics": ["reliability"],
        },
        "modifiability": {
            "name": "Modifiability",
            "measures": [
                "non_complex_file_density",
                "commented_file_density",
                "duplication_absense",
            ],
            "characteristics": ["maintainability"],
        },
    },
    "measures": {
        "passed_tests": {
            "name": "Passed Tests",
            "subcharacteristics": ["testing_status"],
            "characteristics": ["reliability"],
        },
        "test_builds": {
            "name": "Test Builds",
            "subcharacteristics": ["testing_status"],
            "characteristics": ["reliability"],
        },
        "test_coverage": {
            "name": "Test Coverage",
            "subcharacteristics": ["testing_status"],
            "characteristics": ["reliability"],
        },
        "non_complex_file_density": {
            "name": "Non complex file density",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
        },
        "commented_file_density": {
            "name": "Commented file density",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
        },
        "duplication_absense": {
            "name": "Duplication abscense",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
        },
    },
}
