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
        calculate_em1,  # function
        {
            "data": {},
            "MINIMUM_COMPLEX_FILES_DENSITY_THRESHOLD": 1,
            "MAXIMUM_COMPLEX_FILES_DENSITY_THRESHOLD": 10,
        },  # params
        "MINIMUM_COMPLEX_FILES_DENSITY_THRESHOLD is not equal to 0",  # Expected
    ),
    (
        calculate_em1,  # function
        {
            "data": {},
            "MINIMUM_COMPLEX_FILES_DENSITY_THRESHOLD": 0,
            "MAXIMUM_COMPLEX_FILES_DENSITY_THRESHOLD": -10,
        },  # params
        "MINIMUM_COMPLEX_FILES_DENSITY_THRESHOLD is greater or equal to MAXIMUM_COMPLEX_FILES_DENSITY_THRESHOLD",  # Expected
    ),
    (
        calculate_em2,
        {
            "data": {},
            "MINIMUM_COMMENT_DENSITY_THRESHOLD": -1,
            "MAXIMUM_COMMENT_DENSITY_THRESHOLD": 100,
        },  # params
        "MINIMUM_COMMENT_DENSITY_THRESHOLD is lesser than 0",
    ),
    (
        calculate_em2,
        {
            "data": {},
            "MINIMUM_COMMENT_DENSITY_THRESHOLD": 0,
            "MAXIMUM_COMMENT_DENSITY_THRESHOLD": 101,
        },  # params
        "MAXIMUM_COMMENT_DENSITY_THRESHOLD is greater than 100",
    ),
    (
        calculate_em2,
        {
            "data": {},
            "MINIMUM_COMMENT_DENSITY_THRESHOLD": 100,
            "MAXIMUM_COMMENT_DENSITY_THRESHOLD": 99,
        },
        "MINIMUM_COMMENT_DENSITY_THRESHOLD is greater or equal to MAXIMUM_COMMENT_DENSITY_THRESHOLD",
    ),
    (
        calculate_em3,  # function
        {
            "data": {},
            "MINIMUM_DUPLICATED_LINES_THRESHOLD": 1,
            "MAXIMUM_DUPLICATED_LINES_THRESHOLD": 10,
        },  # params
        "MINIMUM_DUPLICATED_LINES_THRESHOLD is not equal to 0",  # Expected
    ),
    (
        calculate_em3,  # function
        {
            "data": {},
            "MINIMUM_DUPLICATED_LINES_THRESHOLD": 0,
            "MAXIMUM_DUPLICATED_LINES_THRESHOLD": -1,
        },  # params
        "MINIMUM_DUPLICATED_LINES_THRESHOLD is greater or equal to MAXIMUM_DUPLICATED_LINES_THRESHOLD",  # Expected
    ),
    (
        calculate_em3,  # function
        {
            "data": {},
            "MINIMUM_DUPLICATED_LINES_THRESHOLD": 0,
            "MAXIMUM_DUPLICATED_LINES_THRESHOLD": 101,
        },  # params
        "MAXIMUM_DUPLICATED_LINES_THRESHOLD is greater than 100",  # Expected
    ),
    (
        calculate_em4,  # function
        {
            "data": {},
            "MINIMUM_PASSED_TESTS_THRESHOLD": 10,
            "MAXIMUM_PASSED_TESTS_THRESHOLD": 1,
        },  # params
        "MINIMUM_PASSED_TESTS_THRESHOLD is not equal to 0",  # Expected
    ),
    (
        calculate_em4,  # function
        {
            "data": {},
            "MINIMUM_PASSED_TESTS_THRESHOLD": 0,
            "MAXIMUM_PASSED_TESTS_THRESHOLD": 0.99,
        },  # params
        "MAXIMUM_PASSED_TESTS_THRESHOLD is not equal to 1",  # Expected
    ),
    (
        calculate_em5,  # function
        {
            "data": {},
            "MINIMUM_FAST_TEST_TIME_THRESHOLD": -1,
            "MAXIMUM_FAST_TEST_TIME_THRESHOLD": 0.99,
        },  # params
        "MINIMUM_FAST_TEST_TIME_THRESHOLD is not equal to 0",  # Expected
    ),
    (
        calculate_em5,  # function
        {
            "data": {},
            "MINIMUM_FAST_TEST_TIME_THRESHOLD": 0,
            "MAXIMUM_FAST_TEST_TIME_THRESHOLD": -10,
        },  # params
        "MINIMUM_FAST_TEST_TIME_THRESHOLD is greater or equal to MAXIMUM_FAST_TEST_TIME_THRESHOLD",  # Expected
    ),
    (
        calculate_em6,  # function
        {
            "data": {},
            "MINIMUM_COVERAGE_THRESHOLD": -1,
            "MAXIMUM_COVERAGE_THRESHOLD": -10,
        },  # params
        "MINIMUM_COVERAGE_THRESHOLD is lesser than 0",  # Expected
    ),
    (
        calculate_em6,  # function
        {
            "data": {},
            "MINIMUM_COVERAGE_THRESHOLD": 90,
            "MAXIMUM_COVERAGE_THRESHOLD": 90,
        },  # params
        "MINIMUM_COVERAGE_THRESHOLD is greater or equal to MAXIMUM_COVERAGE_THRESHOLD",  # Expected
    ),
    (
        calculate_em6,  # function
        {
            "data": {},
            "MINIMUM_COVERAGE_THRESHOLD": 90,
            "MAXIMUM_COVERAGE_THRESHOLD": 900,
        },  # params
        "MAXIMUM_COVERAGE_THRESHOLD is greater than 100",  # Expected
    ),
]
