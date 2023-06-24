INVALID_DIFF_DATA = [
    (
        [1, 1, 1],
        [1, 1],
        "The size between planned and developed release vectors is not equal.",
    ),
    (
        [1, 1],
        [1, 1, 1],
        "The size between planned and developed release vectors is not equal.",
    ),
]

VALID_DIFF_DATA = [
    ([0.7, 0.5, 0.9, 0.6], [0.8, 0.7, 0.95, 0.8], (0.2200666248474033, [0, 0, 0, 0])),
    (
        [0.8, 0.7, 0.95, 0.8],
        [0.7, 0.5, 0.9, 0.6],
        (
            0.18604243256998532,
            [
                0.10000000000000009,
                0.19999999999999996,
                0.04999999999999993,
                0.20000000000000007,
            ],
        ),
    ),
]
