AVAILABLE_PRE_CONFIGS = {
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
                    "duplication_absense": {"name": "Duplicatio abscense"},
                },
            }
        },
    },
}
