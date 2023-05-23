from core.measures_functions import (
    calculate_em1,
    calculate_em2,
    calculate_em3,
    calculate_em4,
    calculate_em5,
    calculate_em6,
)

INVALID_TRESHOLD_DATA = [
    (
        calculate_em1,
        {
            "data": {},
            "min_complex_files_density": 1,
            "max_complex_files_density": 10,
        },
        "min_complex_files_density is not equal to 0",
    ),
    (
        calculate_em1,
        {
            "data": {},
            "min_complex_files_density": 0,
            "max_complex_files_density": -10,
        },
        "min_complex_files_density is greater or equal to max_complex_files_density",
    ),
    (
        calculate_em2,
        {
            "data": {},
            "min_comment_density": -1,
            "max_comment_density": 100,
        },
        "min_comment_density is lesser than 0",
    ),
    (
        calculate_em2,
        {
            "data": {},
            "min_comment_density": 0,
            "max_comment_density": 101,
        },
        "max_comment_density is greater than 100",
    ),
    (
        calculate_em2,
        {
            "data": {},
            "min_comment_density": 100,
            "max_comment_density": 99,
        },
        "min_comment_density is greater or equal to max_comment_density",
    ),
    (
        calculate_em3,
        {
            "data": {},
            "min_duplicated_lines": 1,
            "max_duplicated_lines": 10,
        },
        "min_duplicated_lines is not equal to 0",
    ),
    (
        calculate_em3,
        {
            "data": {},
            "min_duplicated_lines": 0,
            "max_duplicated_lines": -1,
        },
        "min_duplicated_lines is greater or equal to max_duplicated_lines",
    ),
    (
        calculate_em3,
        {
            "data": {},
            "min_duplicated_lines": 0,
            "max_duplicated_lines": 101,
        },
        "max_duplicated_lines is greater than 100",
    ),
    (
        calculate_em4,
        {
            "data": {},
            "min_passed_tests": 10,
            "max_passed_tests": 1,
        },
        "min_passed_tests is not equal to 0",
    ),
    (
        calculate_em4,
        {
            "data": {},
            "min_passed_tests": 0,
            "max_passed_tests": 0.99,
        },
        "max_passed_tests is not equal to 1",
    ),
    (
        calculate_em5,
        {
            "data": {},
            "min_fast_test_time": -1,
            "max_fast_test_time": 0.99,
        },
        "min_fast_test_time is not equal to 0",
    ),
    (
        calculate_em5,
        {
            "data": {},
            "min_fast_test_time": 0,
            "max_fast_test_time": -10,
        },
        "min_fast_test_time is greater or equal to max_fast_test_time",
    ),
    (
        calculate_em6,
        {
            "data": {},
            "MINIMUM_COVERAGE_THRESHOLD": -1,
            "MAXIMUM_COVERAGE_THRESHOLD": -10,
        },
        "MINIMUM_COVERAGE_THRESHOLD is lesser than 0",
    ),
    (
        calculate_em6,
        {
            "data": {},
            "MINIMUM_COVERAGE_THRESHOLD": 90,
            "MAXIMUM_COVERAGE_THRESHOLD": 90,
        },
        "MINIMUM_COVERAGE_THRESHOLD is greater or equal to MAXIMUM_COVERAGE_THRESHOLD",
    ),
    (
        calculate_em6,
        {
            "data": {},
            "MINIMUM_COVERAGE_THRESHOLD": 90,
            "MAXIMUM_COVERAGE_THRESHOLD": 900,
        },
        "MAXIMUM_COVERAGE_THRESHOLD is greater than 100",
    ),
]
