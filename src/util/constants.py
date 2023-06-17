from core import schemas
from core.aggregated_normalized_measures import (
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
                "total_number_of_issues_with_US_label_in_the_last_x_days",
            ],
        },
    },
}

AGGREGATED_NORMALIZED_MEASURES_MAPPING = {
    "non_complex_file_density": {
        "aggregated_normalized_measure": non_complex_files_density,
        "schema": schemas.NonComplexFileDensitySchema,
        "thresholds": ["min_complex_files_density", "max_complex_files_density"],
    },
    "commented_file_density": {
        "aggregated_normalized_measure": commented_files_density,
        "schema": schemas.CommentedFileDensitySchema,
        "thresholds": ["min_comment_density", "max_comment_density"],
    },
    "duplication_absense": {
        "aggregated_normalized_measure": absence_of_duplications,
        "schema": schemas.DuplicationAbsenceSchema,
        "thresholds": ["min_duplicated_lines", "max_duplicated_lines"],
    },
    "passed_tests": {
        "aggregated_normalized_measure": passed_tests,
        "schema": schemas.PassedTestsSchema,
        "thresholds": ["min_passed_tests", "max_passed_tests"],
    },
    "test_builds": {
        "aggregated_normalized_measure": fast_test_builds,
        "schema": schemas.TestBuildsSchema,
        "thresholds": ["min_fast_test_time", "max_fast_test_time"],
    },
    "test_coverage": {
        "aggregated_normalized_measure": test_coverage,
        "schema": schemas.TestCoverageSchema,
        "thresholds": ["min_coverage", "max_coverage"],
    },
    "team_throughput": {
        "aggregated_normalized_measure": ...,
        "schema": schemas.TeamThroughputSchema,
        "thresholds": [],
    },
}
