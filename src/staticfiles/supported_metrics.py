SUPPORTED_MEASURES = [
    {
        "passed_tests": {
            "metrics": [
                "tests",
                "test_failures",
                "test_errors",
            ],
        }
    },
    {
        "test_builds": {
            "metrics": [
                "test_execution_time",
                "tests",
            ],
        }
    },
    {
        "test_coverage": {
            "metrics": [
                "coverage",
            ],
        }
    },
    {
        "non_complex_file_density": {
            "metrics": [
                "functions",
                "complexity",
            ],
        }
    },
    {
        "commented_file_density": {
            "metrics": [
                "comment_lines_density",
            ],
        }
    },
    {
        "duplication_absense": {
            "metrics": [
                "duplicated_lines_density",
            ],
        }
    },
    {
        "team_throughput": {
            "metrics": [
                "total_issues",
                "resolved_issues",
            ],
        }
    },
    # {
    #     "ci_feedback_time": {
    #         "metrics": [
    #             "number_of_build_pipelines_in_the_last_x_days",
    #             "runtime_sum_of_build_pipelines_in_the_last_x_days",
    #         ],
    #     }
    # },
]
