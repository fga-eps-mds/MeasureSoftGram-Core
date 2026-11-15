from core import schemas
from core.aggregated_normalized_measures import (
    absence_of_duplications,
    commented_files_density,
    fast_test_builds,
    non_complex_files_density,
    passed_tests,
    test_coverage,
    team_throughput,
    ci_feedback_time,
    run_time_measure,
    technical_debt_ratio,
    security_rating_measure,
    security_review_rating_measure,
    absence_of_vulnerabilities,
    security_alerts_resolution,
)

AVAILABLE_PRE_CONFIGS = {
    "characteristics": {
        "reliability": {
            "name": "Reliability",
            "subcharacteristics": ["testing_status", "maturity"],
        },
        "maintainability": {
            "name": "Maintainability",
            "subcharacteristics": ["modifiability"],
        },
        "functional_suitability": {
            "name": "Functional Suitability",
            "subcharacteristics": ["functional_completeness"],
        },
        "performance_efficiency": {
            "name": "Performance Efficiency",
            "subcharacteristics": ["time_behaviour", "resource_utilization"],
        },
        "security": {
            "name": "Security",
            "subcharacteristics": ["confidentiality", "integrity"],
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
        "maturity": {
            "name": "Maturity",
            "measures": ["ci_feedback_time"],
            "characteristics": ["reliability"],
        },
        "modifiability": {
            "name": "Modifiability",
            "measures": [
                "non_complex_file_density",
                "commented_file_density",
                "duplication_absense",
                "technical_debt_ratio",
            ],
            "characteristics": ["maintainability"],
        },
        "functional_completeness": {
            "name": "Functional Completeness",
            "measures": ["team_throughput"],
            "characteristics": ["functional_suitability"],
        },
        "time_behaviour": {
            "name": "Time Behaviour",
            "measures": ["response_time"],
            "characteristics": ["performance_efficiency"],
        },
        "resource_utilization": {
            "name": "Resource Utilization",
            "measures": ["cpu_utilization", "memory_utilization"],
            "characteristics": ["performance_efficiency"],
        },
        "confidentiality": {
            "name": "Confidentiality",
            "measures": [
                "security_rating_measure",
                "absence_of_vulnerabilities",
            ],
            "characteristics": ["security"],
        },
        "integrity": {
            "name": "Integrity",
            "measures": [
                "security_review_rating_measure",
                "security_alerts_resolution",
            ],
            "characteristics": ["security"],
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
        "ci_feedback_time": {
            "name": "CI Feedback Time",
            "subcharacteristics": ["maturity"],
            "characteristics": ["reliability"],
            "metrics": ["sum_ci_feedback_times", "total_builds"],
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
        "technical_debt_ratio": {
            "name": "Technical debt ratio",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
            "metrics": ["sqale_debt_ratio"],
        },
        "team_throughput": {
            "name": "Team Throughput",
            "subcharacteristics": ["functional_completeness"],
            "characteristics": ["functional_suitability"],
            "metrics": ["total_issues", "resolved_issues"],
        },
        "response_time": {
            "name": "Response Time",
            "subcharacteristics": ["time_behaviour"],
            "characteristics": ["performance_efficiency"],
            "metrics": ["endpoint_calls", "mean_response_time"],
        },
        "cpu_utilization": {
            "name": "CPU Utilization",
            "subcharacteristics": ["resource_utilization"],
            "characteristics": ["performance_efficiency"],
            "metrics": ["endpoint_calls", "cpu_usage"],
        },
        "memory_utilization": {
            "name": "Memory Utilization",
            "subcharacteristics": ["resource_utilization"],
            "characteristics": ["performance_efficiency"],
            "metrics": ["endpoint_calls", "memory_usage"],
        },
        "security_rating_measure": {
            "name": "Security Rating",
            "subcharacteristics": ["confidentiality"],
            "characteristics": ["security"],
            "metrics": ["security_rating"],
        },
        "absence_of_vulnerabilities": {
            "name": "Absence of vulnerabilities",
            "subcharacteristics": ["confidentiality"],
            "characteristics": ["security"],
            "metrics": ["vulnerabilities", "ncloc"],
        },
        "security_review_rating_measure": {
            "name": "Security Review Rating",
            "subcharacteristics": ["integrity"],
            "characteristics": ["security"],
            "metrics": ["security_review_rating"],
        },
        "security_alerts_resolution": {
            "name": "Security Alerts Resolution",
            "subcharacteristics": ["integrity"],
            "characteristics": ["security"],
            "metrics": ["security_alerts_open", "security_alerts_closed"],
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
    "security_rating_measure": {
        "aggregated_normalized_measure": security_rating_measure,
        "schema": schemas.SecurityRatingSchema,
    },
    "security_review_rating_measure": {
        "aggregated_normalized_measure": security_review_rating_measure,
        "schema": schemas.SecurityReviewRatingSchema,
    },
    "absence_of_vulnerabilities": {
        "aggregated_normalized_measure": absence_of_vulnerabilities,
        "schema": schemas.AbsenceOfVulnerabilitiesSchema,
    },
    "security_alerts_resolution": {
        "aggregated_normalized_measure": security_alerts_resolution,
        "schema": schemas.SecurityAlertsResolutionSchema,
    },
    "technical_debt_ratio": {
        "aggregated_normalized_measure": technical_debt_ratio,
        "schema": schemas.TechnicalDebtRatioSchema,
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
    "ci_feedback_time": {
        "aggregated_normalized_measure": ci_feedback_time,
        "schema": schemas.CIFeedbackTimeSchema,
    },
    "response_time": {
        "aggregated_normalized_measure": run_time_measure,
        "schema": schemas.CompareRunTimeMeasureSchema,
    },
    "cpu_utilization": {
        "aggregated_normalized_measure": run_time_measure,
        "schema": schemas.CompareRunTimeMeasureSchema,
    },
    "memory_utilization": {
        "aggregated_normalized_measure": run_time_measure,
        "schema": schemas.CompareRunTimeMeasureSchema,
    },
}
