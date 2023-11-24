EXTRACTED_MEASURES_DATA = {
    "measures": [
        {
            "key": "passed_tests",
            "metrics":[
                    {
                        "key": "tests",
                        "value":[
                            3.0,
                            1.0,
                            6.0,
                            3.0,
                            17.0,
                            2.0,
                            2.0,
                            7.0,
                            1.0,
                            1.0,
                            1.0,
                            3.0,
                            2.0,
                            3.0,
                            23.0,
                            2.0,
                            3.0,
                            4.0,
                            7.0,
                            2.0,
                        ]
                    },
                    {
                        "key":"test_failures",
                        "value" : [0.0]
                    },
                    {
                        "key": "test_errors",
                        "value" : [0.0]
                    }
                ],
        },
        {
            "key": "test_builds",
            "metrics":[
                {
                    "key":"test_execution_time",
                    "value":[
                        6.0,
                        2.0,
                        18.0,
                        6.0,
                        17.0,
                        969.0,
                        4.0,
                        9.0,
                        1.0,
                        961.0,
                        476.0,
                        5.0,
                        954.0,
                        3.0,
                        24.0,
                        23.0,
                        3.0,
                        7.0,
                        47.0,
                        5.0,
                    ]
                },
                {
                    "key": "tests",
                    "value":[
                        3.0,
                        1.0,
                        6.0,
                        3.0,
                        17.0,
                        2.0,
                        2.0,
                        7.0,
                        1.0,
                        1.0,
                        1.0,
                        3.0,
                        2.0,
                        3.0,
                        23.0,
                        2.0,
                        3.0,
                        4.0,
                        7.0,
                        2.0,
                    ]
                }                
            ]
        }
    ]
}

CALCULATE_MEASURES_RESULT_DATA = {
    "measures": [
        {"key": "passed_tests", "value": 1.0},
        {"key": "test_builds", "value": 0.9995933399758454},
        {"key": "test_coverage", "value": 0.414921875},
        {"key": "non_complex_file_density", "value": 0.43738095238095254},
        {"key": "commented_file_density", "value": 0.04453125},
        {"key": "duplication_absense", "value": 1.0},
    ]
}

CALCULATE_MEASURES_ERROR_INFOS = [
    (
        {"measures": None},
        "error: Failed to validate input.\nschema_errors: {'measures': ['Field may not be null.']}",
    ),
    (
        {
            "measures": [
                {
                    "key": "inexistent",
                    "metrics": [
                            {
                                "key": "inexistent_v2",
                                "value":[1]
                            },
                    ]
                }
            ]
        },
        "Measure inexistent is not supported",    
    ),
    (
        {
            "measures": [
                {
                    "key": "passed_tests",
                    "metrics": [
                            {
                                "key": "inexistent_v3",
                                "value": [1]
                            },     
                        ],
                }
            ]
        },
        "error: Metrics in passed_tests are not valid."
    ),
]

EXTRACTED_SUBCHARACTERISTICS_DATA = {
    "subcharacteristics": [
        {
            "key": "testing_status",
            "measures": [
                {"key": "passed_tests", "value": 1.0, "weight": 33},
                {"key": "test_builds", "value": 0.9995933399758454, "weight": 33},
                {"key": "test_coverage", "value": 0.4515625, "weight": 34},
            ],
        },
        {
            "key": "modifiability",
            "measures": [
                {
                    "key": "non_complex_file_density",
                    "value": 0.5361702127659572,
                    "weight": 33,
                },
                {"key": "commented_file_density", "value": 0.04453125, "weight": 33},
                {"key": "duplication_absense", "value": 1.0, "weight": 34},
            ],
        },
    ]
}

CALCULATE_SUBCHARACTERISTICS_RESULT_DATA = {
    "subcharacteristics": [
        {"key": "testing_status", "value": 0.8507086078793112},
        {"key": "modifiability", "value": 0.6642882099299446},
    ]
}

CALCULATE_SUBCHARACTERISTICS_ERROR_INFOS = [
    (
        {"subcharacteristics": None},
        "error: Failed to validate input.\nschema_errors: {'subcharacteristics': ['Field may not be null.']}",
    ),
]

EXTRACTED_CHARACTERISTICS_DATA = {
    "characteristics": [
        {
            "key": "reliability",
            "subcharacteristics": [{"key": "testing_status", "value": 0.8507086078793112, "weight": 100}],
        },
        {
            "key": "maintainability",
            "subcharacteristics": [{"key": "modifiability", "value": 0.6642882099299446, "weight": 100}],
        },
    ]
}

CALCULATE_CHARACTERISTICS_RESULT_DATA = {
    "characteristics": [
        {"key": "reliability", "value": 0.8507086078793112},
        {"key": "maintainability", "value": 0.6642882099299446},
    ]
}

CALCULATE_CHARACTERISTICS_ERROR_INFOS = [
    (
        {"characteristics": None},
        "error: Failed to validate input.\nschema_errors: {'characteristics': ['Field may not be null.']}",
    )
]

EXTRACTED_TSQMI_DATA = {
    "tsqmi": {
        "key": "tsqmi",
        "characteristics": [
            {"key": "reliability", "value": 0.8507086078793112, "weight": 50},
            {"key": "maintainability", "value": 0.6642882099299446, "weight": 50},
        ],
    }
}

CALCULATE_TSQMI_RESULT_DATA = {"tsqmi": [{"key": "tsqmi", "value": 0.7632116224782893}]}

CALCULATE_TSQMI_ERROR_INFOS = [
    (
        {"tsqmi": None},
        "error: Failed to validate input.\nschema_errors: {'tsqmi': ['Field may not be null.']}",
    )
]
