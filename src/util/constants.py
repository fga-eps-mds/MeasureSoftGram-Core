import core.measures_functions as ems_functions
from core import schemas
from core.interpretation_functions import (
    absence_of_duplications,
    commented_files_density,
    fast_test_builds,
    non_complex_files_density,
    passed_tests,
    test_coverage,
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
        "productivity": {
            "name": "Productivity",
            "subcharacteristics": ["issues_velocity"],
        },
    },
    "subcharacteristics": {
        "testing_status": {
            "name": "Testing Status",
            "measures": [
                "passed_tests",
                "test_builds",
                "test_coverage",
            ],
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
        "issues_velocity": {
            "name": "Issues Velocity",
            "measures": ["team_throughput"],
            "characteristics": ["productivity"],
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
        "team_throughput": {
            "name": "Team Throughput",
            "subcharacteristics": ["functional_completeness"],
            "characteristics": ["functional_suitability"],
            "metrics": [
                "number_of_resolved_issues_with_US_label_in_the_last_x_days",
                "total_number_of_issues_with_US_label_in_the_last_x_days"
            ],
        },
    },
}


MEASURES_INTERPRETATION_MAPPING = {
    "non_complex_file_density": {
        "interpretation_function": non_complex_files_density,
        "calculation_function": ems_functions.calculate_em1,
        "schema": schemas.NonComplexFileDensitySchema,
    },
    "commented_file_density": {
        "interpretation_function": commented_files_density,
        "calculation_function": ems_functions.calculate_em2,
        "schema": schemas.CommentedFileDensitySchema,
    },
    "duplication_absense": {
        "interpretation_function": absence_of_duplications,
        "calculation_function": ems_functions.calculate_em3,
        "schema": schemas.DuplicationAbsenceSchema,
    },
    "passed_tests": {
        "interpretation_function": passed_tests,
        "calculation_function": ems_functions.calculate_em4,
        "schema": schemas.PassedTestsSchema,
    },
    "test_builds": {
        "interpretation_function": fast_test_builds,
        "calculation_function": ems_functions.calculate_em5,
        "schema": schemas.TestBuildsSchema,
    },
    "test_coverage": {
        "interpretation_function": test_coverage,
        "calculation_function": ems_functions.calculate_em6,
        "schema": schemas.TestCoverageSchema,
    },
    "team_throughput": {
        "interpretation_function": ...,
        "calculation_function": ems_functions.calculate_em7,
        "schema": schemas.TeamThroughputSchema,
    },
}
