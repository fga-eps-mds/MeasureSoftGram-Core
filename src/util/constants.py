from core import schemas
from core.aggregated_normalized_measures import (
    absence_of_duplications,
    commented_files_density,
    fast_test_builds,
    non_complex_files_density,
    passed_tests,
    test_coverage,
    team_throughput,
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
        "functional_suitability": {
            "name": "Functional Suitability",
            "subcharacteristics": ["functional_completeness"],
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
        "functional_completeness": {
            "name": "Functional Completeness",
            "measures": ["team_throughput"],
            "characteristics": ["functional_suitability"],
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
                "total_issues",
                "resolved_issues",
            ],
        },
    },
}

AGGREGATED_NORMALIZED_MEASURES_MAPPING = {
    "non_complex_file_density": {
        "aggregated_normalized_measure": non_complex_files_density,
        "schema": schemas.NonComplexFileDensitySchema,
    },
    "commented_file_density": {
        "aggregated_normalized_measure": commented_files_density,
        "schema": schemas.CommentedFileDensitySchema,
    },
    "duplication_absense": {
        "aggregated_normalized_measure": absence_of_duplications,
        "schema": schemas.DuplicationAbsenceSchema,
    },
    "passed_tests": {
        "aggregated_normalized_measure": passed_tests,
        "schema": schemas.PassedTestsSchema,
    },
    "test_builds": {
        "aggregated_normalized_measure": fast_test_builds,
        "schema": schemas.TestBuildsSchema,
    },
    "test_coverage": {
        "aggregated_normalized_measure": test_coverage,
        "schema": schemas.TestCoverageSchema,
    },
    "team_throughput": {
        "aggregated_normalized_measure": team_throughput,
        "schema": schemas.TeamThroughputSchema,
    },
}
