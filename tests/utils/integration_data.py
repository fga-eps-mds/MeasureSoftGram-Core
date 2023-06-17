from tests.test_helpers import read_json

PRE_CONFIGURATION = {
    "_id": "6265b525ab15bc00c4effbd0",
    "name": "pre-config-test-analysis",
    "characteristics": {
        "reliability": {
            "expected_value": 70,
            "weight": 50,
            "subcharacteristics": ["testing_status"],
            "weights": {"testing_status": 100},
        },
        "maintainability": {
            "expected_value": 30,
            "weight": 50,
            "subcharacteristics": ["modifiability"],
            "weights": {"modifiability": 100},
        },
    },
    "subcharacteristics": {
        "testing_status": {
            "weights": {"passed_tests": 100},
            "measures": ["passed_tests"],
        },
        "modifiability": {
            "weights": {"non_complex_file_density": 100},
            "measures": ["non_complex_file_density"],
        },
    },
    "measures": ["passed_tests", "non_complex_file_density"],
}

JSON_FILE = read_json(
    "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-Service-04-12-2022-17-32-35-v1.1.0.json"
)

COMPONENT = {
    "pre_config_id": "6265b525ab15bc00c4effbd0",
    "components": JSON_FILE["components"],
    "language_extension": "py",
}

TEST_PARAMETERS = [
    (
        200,
        "characteristics",
        {
            "maintainability": 0.6000000000000001,
            "reliability": 0.7142857142857143,
        },
    ),
    (
        200,
        "subcharacteristics",
        {
            "modifiability": 0.6000000000000001,
            "testing_status": 0.7142857142857143,
        },
    ),
    (
        200,
        "tsqmi",
        {"tsqmi": 0.6596226503208683},
    ),
]


CALCULATE_SUBCHARACTERISTICS_SUCCESS_DATA = [
    (
        # Calculate one subcharacteristic
        {
            "subcharacteristics": [
                {
                    "key": "testing_status",
                    "measures": [
                        {
                            "key": "passed_tests",
                            "value": 1.0,
                            "weight": 33
                        },
                        {
                            "key": "test_builds",
                            "value": 0.00178,
                            "weight": 33
                        },
                        {
                            "key": "test_coverage",
                            "value": 0.25,
                            "weight": 34
                        }
                    ]
                }
            ]
        },
        {
            "subcharacteristics": [
                {
                    "key": "testing_status",
                    "value": 0.5901748671720202
                }
            ]
        }
    ),
    (
        # Calculate multiples subcharacteristics
        {
            "subcharacteristics": [
                {
                    "key": "modifiability",
                    "measures": [
                        {
                            "key": "non_complex_file_density",
                            "value": 0.675,
                            "weight": 70
                        },
                        {
                            "key": "commented_file_density",
                            "value": 0.2275,
                            "weight": 30
                        }
                    ]
                },
                {
                    "key": "testing_status",
                    "measures": [
                        {
                            "key": "test_builds",
                            "value": 0.00178,
                            "weight": 100
                        }
                    ]
                }
            ]
        },
        {
            "subcharacteristics": [
                {
                    "key": "modifiability",
                    "value": 0.6268617959382247
                },
                {
                    "key": "testing_status",
                    "value": 0.00178
                }
            ]
        }
    )
]


CALCULATE_CHARACTERISTICS_SUCCESS_DATA = [
    (
        # Calculate one characteristic
        {
            "characteristics": [
                {
                    "key": "reliability",
                    "subcharacteristics": [
                        {
                            "key": "testing_status",
                            "value": 0.90,
                            "weight": 100
                        }
                    ]
                }
            ]
        },
        {
            "characteristics": [
                {
                    "key": "reliability",
                    "value": 0.90
                }
            ]
        }
    ),
    (
        # Calculate multiples characteristics
        {
            "characteristics": [
                {
                    "key": "reliability",
                    "subcharacteristics": [
                        {
                            "key": "testing_status",
                            "value": 1.0,
                            "weight": 100
                        }
                    ]
                },
                {
                    "key": "maintainability",
                    "subcharacteristics": [
                        {
                            "key": "modifiability",
                            "value": 0.675,
                            "weight": 100
                        }
                    ]
                }
            ]
        },
        {
            "characteristics": [
                {
                    "key": "reliability",
                    "value": 1.0
                },
                {
                    "key": "maintainability",
                    "value": 0.675
                }
            ]
        }
    )
]


METRICS_LIST = [
    {
        "key": "test_errors",
        "value": 0.0,
        "measure_key": "passed_tests"
    },
    {
        "key": "test_failures",
        "value": 0.0,
        "measure_key": "passed_tests"
    },
    {
        "key": "tests",
        "value": 1.0,
        "measure_key": "passed_tests"
    },
    {
        "key": "test_execution_time",
        "value": 6.0,
        "measure_key": "test_builds"
    },
    {
        "key": "coverage",
        "value": [64.3, 100.0, 100.0, 85.7, 100.0],
        "measure_key": "test_coverage"
    },
    {
        "key": "complexity",
        "value": [3.0, 0.0, 0.0, 1.0, 0.0],
        "measure_key": "non_complex_file_density"
    },
    {
        "key": "functions",
        "value": [3.0, 0.0, 0.0, 1.0, 0.0],
        "measure_key": "non_complex_file_density"
    },
    {
        "key": "comment_lines_density",
        "value": [0.0, 0.0, 0.0, 0.0, 0.0],
        "measure_key": "commented_file_density"
    },
    {
        "key": "duplicated_lines_density",
        "value": [0.0, 0.0, 0.0, 0.0, 0.0],
        "measure_key": "duplication_absense"
    },
    {
        "key": "number_of_resolved_issues_with_US_label_in_the_last_x_days",
        "value": 1.0,
        "measure_key": "team_throughput"
    },
    {
        "key": "total_number_of_issues_with_US_label_in_the_last_x_days",
        "value": 29.0,
        "measure_key": "team_throughput"
    }
]


CALCULATE_TSQMI_SUCCESS_DATA = [
    (
        {
            "pre_config":
                {
                    "characteristics": [
                        {
                            "key": "reliability",
                            "weight": 51.0,
                            "subcharacteristics": [
                                {
                                    "key": "testing_status",
                                    "weight": 100.0,
                                    "measures": [
                                        {
                                            "key": "passed_tests",
                                            "weight": 40
                                        },
                                        {
                                            "key": "test_builds",
                                            "weight": 60
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "key": "maintainability",
                            "weight": 49.0,
                            "subcharacteristics": [
                                {
                                    "key": "modifiability",
                                    "weight": 100.0,
                                    "measures": [
                                        {
                                            "key": "non_complex_file_density",
                                            "weight": 100
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
            "metrics": METRICS_LIST,
        },
        {
            "value": 0.4713879251478593,
        }
    ),
    (
        {
            "pre_config":
                {
                    "characteristics": [
                        {
                            "key": "reliability",
                            "weight": 50.0,
                            "subcharacteristics": [
                                {
                                    "key": "testing_status",
                                    "weight": 100.0,
                                    "measures": [
                                        {
                                            "key": "passed_tests",
                                            "weight": 33.34
                                        },
                                        {
                                            "key": "test_builds",
                                            "weight": 33.33
                                        },
                                        {
                                            "key": "test_coverage",
                                            "weight": 33.33
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "key": "maintainability",
                            "weight": 30.0,
                            "subcharacteristics": [
                                {
                                    "key": "modifiability",
                                    "weight": 100.0,
                                    "measures": [
                                        {
                                            "key": "non_complex_file_density",
                                            "weight": 50.0
                                        },
                                        {
                                            "key": "commented_file_density",
                                            "weight": 30.0
                                        },
                                        {
                                            "key": "duplication_absense",
                                            "weight": 20.0
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "key": "functional_suitability",
                            "weight": 20.0,
                            "subcharacteristics": [
                                {
                                    "key": "functional_completeness",
                                    "weight": 100.0,
                                    "measures": [
                                        {
                                            "key": "team_throughput",
                                            "weight": 100.0
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
            "metrics": METRICS_LIST,
        },
        {
            "value": 0.6363635698376492,
        }
    ),
]


CALCULATE_ENTITY_INVALID_DATA = [
    (
        # Missing field `measures`
        "subcharacteristics",
        {
            "subcharacteristics": [
                {
                    "key": "testing_status",
                    "value": 0.5
                }
            ]
        }
    ),
    (
        # Missing field `weight` of the measure
        "subcharacteristics",
        {
            "subcharacteristics": [
                {
                    "key": "testing_status",
                    "measures": [
                        {
                            "key": "passed_tests",
                            "value": 0.00178
                        }
                    ]
                }
            ]
        }
    ),
    (
        # The subcharacteristic value must be between 0 and 1
        "characteristics",
        {
            "characteristics": [
                {
                    "name": "reliability",
                    "subcharacteristics": [
                        {
                            "key": "testing_status",
                            "value": 2.5,
                            "weight": 100
                        }
                    ]
                }
            ]
        }
    ),
    (
        # Invalid field `measures` (must be `subcharacteristics`)
        "characteristics",
        {
            "characteristics": [
                {
                    "key": "reliability",
                    "measures": [
                        {
                            "key": "test_builds",
                            "value": 0.475,
                            "weight": 100
                        }
                    ]
                }
            ]
        }
    ),
    (
        # Missing field `pre_config`
        "tsqmi",
        {
            "metrics": METRICS_LIST,
        }
    ),
    (
        # Typo in field `pre-config` (must be `pre_config`)
        "tsqmi",
        {
            "pre-config":
                {
                    "characteristics": [
                        {
                            "key": "reliability",
                            "weight": 100.0,
                            "subcharacteristics": [
                                {
                                    "key": "testing_status",
                                    "weight": 100.0,
                                    "measures": [
                                        {
                                            "key": "passed_tests",
                                            "weight": 100.0
                                        },
                                    ]
                                }
                            ]
                        }
                    ]
                },
            "metrics": METRICS_LIST,
        }
    ),
]
