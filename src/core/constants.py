from src.core.interpretation_functions import (
    non_complex_files_density,
    test_coverage,
    commented_files_density,
    absence_of_duplications,
    passed_tests,
    calculate_em4,
    fast_test_builds,
)
from src.core.schemas import (
    PassedTestsSchema,
)

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
            "metrics": ["tests", "test_errors", "test_failures"],
        },
        "test_builds": {
            "name": "Test Builds",
            "subcharacteristics": ["testing_status"],
            "characteristics": ["reliability"],
            "metrics": ["tests", "test_execution_time"],
        },
        "test_coverage": {
            "name": "Test Coverage",
            "subcharacteristics": ["testing_status"],
            "characteristics": ["reliability"],
            "metrics": ["coverage"],
        },
        "non_complex_file_density": {
            "name": "Non complex file density",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
            "metrics": ["complexity", "functions"],
        },
        "commented_file_density": {
            "name": "Commented file density",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
            "metrics": ["comment_lines_density"],
        },
        "duplication_absense": {
            "name": "Duplication abscense",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
            "metrics": ["duplicated_lines_density"],
        },
    },
}


MEASURES_INTERPRETATION_MAPPING = {
    "passed_tests": {
        "interpretation_function": passed_tests,
        "calculation_function": calculate_em4,
        "schema": PassedTestsSchema,
    },
    "test_builds": fast_test_builds,
    "test_coverage": test_coverage,
    "non_complex_file_density": non_complex_files_density,
    "commented_file_density": commented_files_density,
    "duplication_absense": absence_of_duplications,
}
