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
        0.0010166666666666666,
    ),
    (
        "test_coverage",
        0.752962962962963,
    ),
    (
        "passed_tests",
        0.7142857142857143
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
