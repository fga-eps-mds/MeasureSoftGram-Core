SONARQUBE_SUPPORTED_MEASURES = [
    "passed_tests": {
        "metrics": [
            {"key": "tests"},
            {"key": "test_failures"},
            {"key": "test_errors"},
        ],
    },
    "test_builds": {
        "metrics": [
            {"key": "test_execution_time"},
        ],
    },
    "test_coverage": {
        "metrics": [
            {"key": "coverage"},
        ],
    },
    "non_complex_file_density": {
        "metrics": [
            {"key": "functions"},
            {"key": "complexity"},
        ],
    },
    "commented_file_density": {
        "metrics": [
            {"key": "comment_lines_density"},
        ],
    },
    "duplication_absense": {
        "metrics": [
            {"key": "duplicated_lines_density"},
        ],
    },
    # "ci_feedback_time": {
    #     "metrics": [
    #         {"key": "number_of_build_pipelines_in_the_last_x_days"},
    #         {"key": "runtime_sum_of_build_pipelines_in_the_last_x_days"},
    #     ],
    # },
    "team_throughput": {
        "metrics": [
            {"key": "number_of_resolved_issues_with_US_label_in_the_last_x_days"},
            {"key": "total_number_of_issues_with_US_label_in_the_last_x_days"},
        ],
    },
]
