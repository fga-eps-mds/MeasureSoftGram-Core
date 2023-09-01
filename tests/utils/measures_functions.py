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
            "min_threshold": 1,
            "max_threshold": 10,
        },
        "min_threshold is not equal to 0",
    ),
    (
        calculate_em1,
        {
            "data": {},
            "min_threshold": 0,
            "max_threshold": -10,
        },
        "min_threshold is greater or equal to max_threshold",
    ),
    (
        calculate_em2,
        {
            "data": {},
            "min_threshold": -1,
            "max_threshold": 100,
        },
        "min_threshold is lesser than 0",
    ),
    (
        calculate_em2,
        {
            "data": {},
            "min_threshold": 0,
            "max_threshold": 101,
        },
        "max_threshold is greater than 100",
    ),
    (
        calculate_em2,
        {
            "data": {},
            "min_threshold": 100,
            "max_threshold": 99,
        },
        "min_threshold is greater or equal to max_threshold",
    ),
    (
        calculate_em3,
        {
            "data": {},
            "min_threshold": 1,
            "max_threshold": 10,
        },
        "min_threshold is not equal to 0",
    ),
    (
        calculate_em3,
        {
            "data": {},
            "min_threshold": 0,
            "max_threshold": -1,
        },
        "min_threshold is greater or equal to max_threshold",
    ),
    (
        calculate_em3,
        {
            "data": {},
            "min_threshold": 0,
            "max_threshold": 101,
        },
        "max_threshold is greater than 100",
    ),
    (
        calculate_em4,
        {
            "data": {},
            "min_threshold": 10,
            "max_threshold": 1,
        },
        "min_threshold is not equal to 0",
    ),
    (
        calculate_em4,
        {
            "data": {},
            "min_threshold": 0,
            "max_threshold": 0.99,
        },
        "max_threshold is not equal to 1",
    ),
    (
        calculate_em5,
        {
            "data": {},
            "min_threshold": -1,
            "max_threshold": 0.99,
        },
        "min_threshold is not equal to 0",
    ),
    (
        calculate_em5,
        {
            "data": {},
            "min_threshold": 0,
            "max_threshold": -10,
        },
        "min_threshold is greater or equal to max_threshold",
    ),
    (
        calculate_em6,
        {
            "data": {},
            "min_threshold": -1,
            "max_threshold": -10,
        },
        "min_threshold is lesser than 0",
    ),
    (
        calculate_em6,
        {
            "data": {},
            "min_threshold": 90,
            "max_threshold": 90,
        },
        "min_threshold is greater or equal to max_threshold",
    ),
    (
        calculate_em6,
        {
            "data": {},
            "min_threshold": 90,
            "max_threshold": 900,
        },
        "max_threshold is greater than 100",
    ),
]
