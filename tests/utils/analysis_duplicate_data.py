EXTRACTED_MEASURES_DATA = {
    'measures':
    [
        {'key': 'passed_tests', 'parameters': {
            'tests': [
                3.0, 1.0, 6.0, 3.0, 17.0, 2.0, 2.0, 7.0, 1.0, 1.0, 1.0, 3.0, 2.0,
                3.0, 23.0, 2.0, 3.0, 4.0, 7.0, 2.0
            ], 'test_failures': 0.0, 'test_errors': 0.0}},
        {'key': 'test_builds', 'parameters': {
            'test_execution_time': [
                6.0, 2.0, 18.0, 6.0, 17.0, 969.0, 4.0, 9.0, 1.0, 961.0, 476.0, 5.0,
                954.0, 3.0, 24.0, 23.0, 3.0, 7.0, 47.0, 5.0
            ],
            'tests': [
                3.0, 1.0, 6.0, 3.0, 17.0, 2.0, 2.0, 7.0, 1.0, 1.0, 1.0, 3.0, 2.0,
                3.0, 23.0, 2.0, 3.0, 4.0, 7.0, 2.0
            ]
        }},
        {'key': 'test_coverage', 'parameters': {'coverage': [
            0.0, 0.0, 0.0, 0.0, 0.0, 44.4, 23.5, 100.0, 100.0, 50.0, 77.8, 100.0,
            100.0, 91.4, 100.0, 43.8, 0.0, 55.6, 26.7, 100.0, 100.0, 100.0, 0.0,
            100.0, 64.7, 86.6, 0.0, 61.9, 91.8, 94.4, 82.5, 13.3
        ]}},
        {'key': 'non_complex_file_density', 'parameters': {
            'functions': [
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 3.0, 3.0, 2.0, 1.0, 1.0, 0.0, 8.0, 10.0, 1.0, 1.0,
                1.0, 1.0, 1.0, 3.0, 1.0, 3.0, 1.0, 1.0, 1.0, 1.0, 3.0, 7.0, 7.0, 2.0,
                4.0, 4.0, 14.0, 6.0, 3.0
            ],
            'complexity': [
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 4.0, 4.0, 6.0, 1.0, 2.0, 0.0, 14.0, 23.0, 1.0, 6.0,
                2.0, 2.0, 1.0, 11.0, 5.0, 15.0, 1.0, 4.0, 5.0, 1.0, 13.0, 13.0, 19.0,
                3.0, 7.0, 11.0, 51.0, 19.0, 10.0
            ]}},
        {'key': 'commented_file_density', 'parameters': {'comment_lines_density': [
            0.0, 0.0, 0.0, 5.7, 2.1, 4.8, 0.0, 0.0, 38.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 8.5, 0.0, 5.9, 0.0, 0.0, 0.0, 6.4, 0.0, 1.4, 14.8, 16.7, 35.3, 0.0,
            0.0, 0.0, 0.0
        ]}},
        {'key': 'duplication_absense', 'parameters': {'duplicated_lines_density': [
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0
        ]}}]
}

CALCULATE_MEASURES_RESPONSE_DATA = {
    'measures':
    [
        {'key': 'passed_tests', 'value': 1.0},
        {'key': 'test_builds', 'value': 0.9999959333997583},
        {'key': 'test_coverage', 'value': 0.4515625},
        {'key': 'non_complex_file_density', 'value': 0.5361702127659572},
        {'key': 'commented_file_density', 'value': 0.04453125},
        {'key': 'duplication_absense', 'value': 1.0}
    ]
}


CALCULATE_MEASURES_ERROR_INFOS = [
    (
        {'measures': None},
        "Failed to validate request"
    ),
    (
        {'measures': [{'key': 'inexistent', 'parameters': {'inexistent_v2': [1]}}]},
        "Measure inexistent is not supported"
    ),
    (
        {'measures': [{'key': 'duplication_absense', 'parameters': {'duplicated_lines_density': [None]}}]},
        "Metric parameters duplication_absense are not valid"
    ),
]

EXTRACTED_SUBCHARACTERISTICS_DATA = {
    'subcharacteristics': [
        {'key': 'testing_status', 'measures': [
            {'key': 'passed_tests', 'value': 1.0, 'weight': 33},
            {'key': 'test_builds', 'value': 0.9999959333997583, 'weight': 33},
            {'key': 'test_coverage', 'value': 0.4515625, 'weight': 34}]},
        {'key': 'modifiability', 'measures': [
            {'key': 'non_complex_file_density', 'value': 0.5361702127659572, 'weight': 33},
            {'key': 'commented_file_density', 'value': 0.04453125, 'weight': 33},
            {'key': 'duplication_absense', 'value': 1.0, 'weight': 34}]}
    ]
}
CALCULATE_SUBCHARACTERISTICS_RESPONSE_DATA = {
    'subcharacteristics': [
        {'key': 'testing_status', 'value': 0.8508631402592323},
        {'key': 'modifiability', 'value': 0.6642882099299446}
    ]
}
CALCULATE_SUBCHARACTERISTICS_ERROR_INFOS = [
    (
        {'subcharacteristics': None},
        "Failed to validate request"
    )
]

EXTRACTED_CHARACTERISTICS_DATA = {
    'characteristics': [
        {'key': 'reliability', 'subcharacteristics': [
            {'key': 'testing_status', 'value': 0.8508631402592323, 'weight': 100}]},
        {'key': 'maintainability', 'subcharacteristics': [
            {'key': 'modifiability', 'value': 0.6642882099299446, 'weight': 100}]}
    ]
}
CALCULATE_CHARACTERISTICS_RESPONSE_DATA = {
    'characteristics': [
        {'key': 'reliability', 'value': 0.8508631402592323},
        {'key': 'maintainability', 'value': 0.6642882099299446}
    ]
}
CALCULATE_CHARACTERISTICS_ERROR_INFOS = [
    (
        {'characteristics': None},
        "Failed to validate request"
    )
]

EXTRACTED_SQC_DATA = {
    'sqc': {'key': 'sqc', 'characteristics': [
        {'key': 'reliability', 'value': 0.8508631402592323, 'weight': 50},
        {'key': 'maintainability', 'value': 0.6642882099299446, 'weight': 50}
    ]}
}
CALCULATE_SQC_RESPONSE_DATA = {
    'sqc': [
        {'key': 'sqc', 'value': 0.76329774967038}
    ]
}
CALCULATE_SQC_ERROR_INFOS = [
    (
        {'sqc': None},
        "Failed to validate request"
    )
]
