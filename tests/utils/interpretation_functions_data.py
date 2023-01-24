from core.interpretation_functions import (
    non_complex_files_density,
    commented_files_density,
    absence_of_duplications,
    test_coverage as interpret_test_coverage,
    passed_tests,
    fast_test_builds,
)

INVALID_METRICS_TEST_DATA = [
    (
        non_complex_files_density,
        {"complexity": [14], "functions": [None]},
        "\"functions\" has an invalid metric value"
    ),
    (
        non_complex_files_density,
        {"complexity": [None], "functions": [15]},
        "\"complexity\" has an invalid metric value"
    ),
    (
        commented_files_density,
        {"comment_lines_density": [None]},
        "\"comment_lines_density\" has an invalid metric value"
    ),
    (
        commented_files_density,
        {"comment_lines_density": ["abc"]},
        "\"comment_lines_density\" has an invalid metric value"
    ),
    (
        absence_of_duplications,
        {"duplicated_lines_density": [None]},
        "\"duplicated_lines_density\" has an invalid metric value"
    ),
    (
        absence_of_duplications,
        {"duplicated_lines_density": ["abc"]},
        "\"duplicated_lines_density\" has an invalid metric value"
    ),
    (
        interpret_test_coverage,
        {"coverage": [None]},
        "\"coverage\" has an invalid metric value"
    ),
    (
        interpret_test_coverage,
        {"coverage": ["abc"]},
        "\"coverage\" has an invalid metric value"
    ),
    (
        fast_test_builds,
        {"test_execution_time": [0.45], "tests": [None]},
        "\"tests\" has an invalid metric value"
    ),
    (
        fast_test_builds,
        {"test_execution_time": [None], "tests": [0.58]},
        "\"test_execution_time\" has an invalid metric value"
    ),
    (
        passed_tests,
        {"tests": [None], "test_errors": 0.0, "test_failures": 0.0},
        "\"tests\" has an invalid metric value"
    ),
    (
        passed_tests,
        {"tests": [0.45], "test_errors": 'abc', "test_failures": 0.0},
        "\"test_errors\" has an invalid metric value"
    ),
    (
        passed_tests,
        {"tests": [0.45], "test_errors": 0.0, "test_failures": None},
        "\"test_failures\" has an invalid metric value"
    ),
]

SUCCESS_TEST_DATA = [
    (
        non_complex_files_density,
        {
            'functions': [
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 3.0, 3.0, 2.0, 1.0, 1.0, 0.0, 8.0, 10.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.0, 1.0, 3.0,
                1.0, 1.0, 1.0, 1.0, 3.0, 7.0, 7.0, 2.0, 4.0, 4.0, 14.0, 6.0, 3.0
            ],
            'complexity': [
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 4.0, 4.0, 6.0, 1.0, 2.0, 0.0, 14.0, 23.0, 1.0, 6.0, 2.0, 2.0, 1.0, 11.0, 5.0,
                15.0, 1.0, 4.0, 5.0, 1.0, 13.0, 13.0, 19.0, 3.0, 7.0, 11.0, 51.0, 19.0, 10.0
            ]
        },
        0.5361702127659572,
    ),
    (
        commented_files_density,
        {'comment_lines_density': [
            0.0, 0.0, 0.0, 5.7, 2.1, 4.8, 0.0, 0.0, 38.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 8.5,
            0.0, 5.9, 0.0, 0.0, 0.0, 6.4, 0.0, 1.4, 14.8, 16.7, 35.3, 0.0, 0.0, 0.0, 0.0
        ]},
        0.04453125,
    ),
    (
        absence_of_duplications,
        {
            'duplicated_lines_density': [
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            ]
        },
        1.0,
    ),
    (
        passed_tests,
        {'test_failures': 0.0, 'test_errors': 0.0, 'tests': [
            3.0, 1.0, 6.0, 3.0, 17.0, 2.0, 2.0, 7.0, 1.0, 1.0, 1.0, 3.0, 2.0, 3.0, 23.0, 2.0, 3.0, 4.0, 7.0, 2.0]},
        1.0,
    ),
    (
        fast_test_builds,
        {
            'test_execution_time': [
                6.0, 2.0, 18.0, 6.0, 17.0, 969.0, 4.0, 9.0, 1.0, 961.0, 476.0, 5.0, 954.0,
                3.0, 24.0, 23.0, 3.0, 7.0, 47.0, 5.0
            ],
            'tests': [
                3.0, 1.0, 6.0, 3.0, 17.0, 2.0, 2.0, 7.0, 1.0, 1.0, 1.0, 3.0, 2.0, 3.0,
                23.0, 2.0, 3.0, 4.0, 7.0, 2.0
            ]
        },
        0.9999959333997583,
    ),
    (
        interpret_test_coverage,
        {'coverage': [
            0.0, 0.0, 0.0, 0.0, 0.0, 44.4, 23.5, 100.0, 100.0, 50.0, 77.8, 100.0,
            100.0, 91.4, 100.0, 43.8, 0.0, 55.6, 26.7, 100.0, 100.0, 100.0, 0.0,
            100.0, 64.7, 86.6, 0.0, 61.9, 91.8, 94.4, 82.5, 13.3
        ]},
        0.4515625,
    )
]

TEST_ROOT_DIR_TEST_DATA = [
    (
        "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-CLI-04-13-2022-02-13-37-v1.1.1.json",
        37,
        "py",
    ),
    (
        "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-Service-04-12-2022-17-32-35-v1.1.0.json",
        7,
        "py",
    ),
]
