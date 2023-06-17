# flake8: noqa
# pylint: skip-file
DEFAULT_PRE_CONFIG = {
    "characteristics": [
        {
            "key": "reliability",
            "weight": 50,
            "subcharacteristics": [
                {
                    "key": "testing_status",
                    "weight": 100,
                    "measures": [
                        {
                            "key": "passed_tests",
                            "weight": 33,
                            "min_passed_tests": 0,
                            "max_passed_tests": 1,
                        },
                        {
                            "key": "test_builds",
                            "weight": 33,
                            "min_fast_test_time": 0,
                            "max_fast_test_time": 300000,
                        },
                        {
                            "key": "test_coverage",
                            "weight": 34,
                            "min_coverage": 60,
                            "max_coverage": 100,
                        },
                    ],
                }
            ],
        },
        {
            "key": "maintainability",
            "weight": 50,
            "subcharacteristics": [
                {
                    "key": "modifiability",
                    "weight": 100,
                    "measures": [
                        {
                            "key": "non_complex_file_density",
                            "weight": 33,
                            "min_complex_files_density": 0,
                            "max_complex_files_density": 10,
                        },
                        {
                            "key": "commented_file_density",
                            "weight": 33,
                            "min_comment_density": 10,
                            "max_comment_density": 30,
                        },
                        {
                            "key": "duplication_absense",
                            "weight": 34,
                            "min_duplicated_lines": 0,
                            "max_duplicated_lines": 5,
                        },
                    ],
                }
            ],
        },
        # {
        #   "key": "functional_suitability",
        #   "weight": 34.0,
        #   "subcharacteristics": [
        #     {
        #       "key": "functional_completeness",
        #       "weight": 100.0,
        #       "measures": [
        #         {
        #           "key": "team_throughput",
        #           "weight": 100.0
        #         }
        #       ]
        #     }
        #   ]
        # }
    ]
}
