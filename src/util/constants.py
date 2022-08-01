from src.core.interpretation_functions import (
    non_complex_files_density,
    test_coverage,
    commented_files_density,
    absence_of_duplications,
    passed_tests,
    fast_test_builds,
    team_throughput
)
from src.core.measures_functions import (
    calculate_em1, calculate_em2, calculate_em3, calculate_em4, calculate_em5, calculate_em6, calculate_em7
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
            "subcharacteristics": ["issues_velocity"],
            "characteristics": ["productivity"],
            "metrics": ["number_of_resolved_issues", "total_number_of_issues"],
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
        "calculation_function": calculate_em5,
        "schema": schemas.TestBuildsSchema,
    },
    "test_coverage": {
        "interpretation_function": test_coverage,
        "calculation_function": calculate_em6,
        "schema": schemas.TestCoverageSchema,
    },
    "non_complex_file_density": {
        "interpretation_function": non_complex_files_density,
        "calculation_function": calculate_em1,
        "schema": schemas.NonComplexFileDensitySchema,
    },
    "commented_file_density": {
        "interpretation_function": commented_files_density,
        "calculation_function": calculate_em2,
        "schema": schemas.CommentedFileDensitySchema,
    },
    "duplication_absense": {
        "interpretation_function": absence_of_duplications,
        "calculation_function": calculate_em3,
        "schema": schemas.DuplicationAbsenceSchema,
    },
    "team_throughput": {
        "interpretation_function": team_throughput,
        "calculation_function": calculate_em7,
        "schema": schemas.TeamThroughputSchema,
    }
}
