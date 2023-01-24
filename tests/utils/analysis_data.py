from tests.test_helpers import create_file_df

JSON_LIST = [
    "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-Service-04-12-2022-17-32-35-v1.1.0.json"
]

SUBS = {
    "testing_status": {
        "measures": ["test_builds", "test_coverage", "passed_tests"],
        "weights": {
            "test_builds": 0.3333,
            "test_coverage": 0.3333,
            "passed_tests": 0.3333,
        },
    }
}

MEASURES = {
    "test_builds": 0.0010166666666666666,
    "test_coverage": 0.5647222222222222,
    "passed_tests": 0.7142857142857143,
}

CHARACTERISTICS = {
    "reliability": {
        "weight": 1.0,
        "subcharacteristics": ["testing_status"],
        "weights": {"testing_status": 1.0},
    },
}

FILES_DF = create_file_df(
    JSON_LIST,
    "py",
)

CALCULATE_MEASURES_DATA = [
    (
        "test_builds",
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
        "test_coverage",
        {'coverage': [
            0.0, 0.0, 0.0, 0.0, 0.0, 44.4, 23.5, 100.0, 100.0, 50.0, 77.8, 100.0,
            100.0, 91.4, 100.0, 43.8, 0.0, 55.6, 26.7, 100.0, 100.0, 100.0, 0.0,
            100.0, 64.7, 86.6, 0.0, 61.9, 91.8, 94.4, 82.5, 13.3
        ]},
        0.4515625,
    ),
    (
        "passed_tests",
        {'test_failures': 0.0, 'test_errors': 0.0, 'tests': [
            3.0, 1.0, 6.0, 3.0, 17.0, 2.0, 2.0, 7.0, 1.0, 1.0, 1.0, 3.0, 2.0, 3.0, 23.0, 2.0, 3.0, 4.0, 7.0, 2.0]},
        1.0
    ),
]

RESOLVE_LEVEL_DATA = [
    (
        SUBS,
        MEASURES,
        "measures",
        0.525711,
    ),
]

MAKE_ANALYSIS_DATA = [
    (
        MEASURES,
        SUBS,
        CHARACTERISTICS,
        [
            0.525711,
            0.525711,
            0.525711,
        ],
        [
            "testing_status",
            "reliability",
            "sqc",
        ]
    ),
]
