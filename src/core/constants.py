from src.core.interpretation_functions import (
    non_complex_files_density,
    test_coverage,
    commented_files_density,
    absence_of_duplications,
    passed_tests,
    calculate_em4,
    fast_test_builds,
)
from src.core import schemas

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
            "metrics": ["test_execution_time"],
        },
        "test_coverage": {
            "name": "Test Coverage",
            "subcharacteristics": ["testing_status"],
            "characteristics": ["reliability"],
            "metrics": ["tests", "coverage"],
        },
        "non_complex_file_density": {
            "name": "Non complex file density",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
            "metrics": ["tests", "complexity", "functions"],
        },
        "commented_file_density": {
            "name": "Commented file density",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
            "metrics": ["tests", "comment_lines_density"],
        },
        "duplication_absense": {
            "name": "Duplication abscense",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
            "metrics": ["tests", "duplicated_lines_density"],
        },
    },
}


MEASURES_INTERPRETATION_MAPPING = {
    "passed_tests": {
        "interpretation_function": passed_tests,
        "calculation_function": calculate_em4,
        "schema": schemas.PassedTestsSchema,
    },
    "test_builds": {
        "interpretation_function": fast_test_builds,
        "calculation_function": ...,
        "schema": schemas.TestBuildsSchema,
    },
    "test_coverage": {
        "interpretation_function": test_coverage,
        "calculation_function": ...,
        "schema": schemas.TestCoverageSchema,
    },
    "non_complex_file_density": {
        "interpretation_function": non_complex_files_density,
        "calculation_function": ...,
        "schema": schemas.NonComplexFileDensitySchema,
    },
    "commented_file_density": {
        "interpretation_function": commented_files_density,
        "calculation_function": ...,
        "schema": schemas.CommentedFileDensitySchema,
    },
    "duplication_absense": {
        "interpretation_function": absence_of_duplications,
        "calculation_function": ...,
        "schema": schemas.DuplicationAbsenceSchema,
    },
}
