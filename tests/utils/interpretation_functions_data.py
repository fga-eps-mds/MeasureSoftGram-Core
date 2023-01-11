from core.interpretation_functions import (
    non_complex_files_density,
    commented_files_density,
    absence_of_duplications,
    test_coverage as interpret_test_coverage,
    passed_tests,
    fast_test_builds,
)

import pandas as pd

INVALID_METRICS_TEST_DATA = [
    (
        non_complex_files_density,
        "tests/unit/data/zero_number_of_files.json",
        "The number of files is lesser or equal than 0",
        "py",
    ),
    (
        non_complex_files_density,
        "tests/unit/data/zero_number_of_functions.json",
        "The number of functions of all files is lesser or equal than 0",
        "js",
    ),
    (
        non_complex_files_density,
        "tests/unit/data/zero_cyclomatic_complexity.json",
        "The cyclomatic complexity of all files is lesser or equal than 0",
        "js",
    ),
    (
        commented_files_density,
        "tests/unit/data/zero_number_of_files.json",
        "The number of files is lesser or equal than 0",
        "py",
    ),
    (
        absence_of_duplications,
        "tests/unit/data/zero_number_of_files.json",
        "The number of files is lesser or equal than 0",
        "py",
    ),
    (
        interpret_test_coverage,
        "tests/unit/data/zero_number_of_files.json",
        "The number of files is lesser or equal than 0",
        "py",
    ),
    (
        non_complex_files_density,
        "tests/unit/data/invalid_complexity_value.json",
        '"complexity" has an invalid metric value',
        "py",
    ),
    (
        commented_files_density,
        "tests/unit/data/invalid_commented_lines_density.json",
        '"comment_lines_density" has an invalid metric value',
        "py",
    ),
]

SUCCESS_TEST_DATA = [
    (
        non_complex_files_density,
        "tests/unit/data/fga-eps-mds_2021-2-SiGeD-Frontend-03-15-2022-23_57_08.json",
        0.6234939759036154,
        "js",
    ),
    (
        non_complex_files_density,
        "tests/unit/data/fga-eps-mds-2020_2-Projeto-Kokama-Usuario-17-04-2021.json",
        0.9,
        "js",
    ),
    (
        non_complex_files_density,
        "tests/unit/data/fga-eps-mds-2020_2-Lend.it-Raleway-user-13-04-2021.json",
        0.5785714285714286,
        "js",
    ),
    (
        commented_files_density,
        "tests/unit/data/fga-eps-mds-2020_2-Projeto-Kokama-Usuario-17-04-2021.json",
        0.0,
        "js",
    ),
    (
        commented_files_density,
        "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-CLI-04-13-2022-02-13-37-v1.1.1.json",
        0.0,
        "py",
    ),
    (
        commented_files_density,
        "tests/unit/data/fga-eps-mds-2020_2-Lend.it-Raleway-user-13-04-2021.json",
        0.0,
        "js",
    ),
    (
        absence_of_duplications,
        "tests/unit/data/fga-eps-mds_2021-2-SiGeD-Frontend-03-15-2022-23_57_08.json",
        0.9096385542168675,
        "js",
    ),
    (
        absence_of_duplications,
        "tests/unit/data/fga-eps-mds-2020_2-Projeto-Kokama-Usuario-17-04-2021.json",
        1.0,
        "js",
    ),
    (
        absence_of_duplications,
        "tests/unit/data/fga-eps-mds-2020_2-Lend.it-Raleway-user-13-04-2021.json",
        1.0,
        "js",
    ),
    # (
    #     interpret_test_coverage,
    #     "tests/unit/data/fga-eps-mds_2021-2-SiGeD-Frontend-03-15-2022-23_57_08.json",
    #     0.0,
    #     "js",
    # ),
    (
        interpret_test_coverage,
        "tests/unit/data/between_zero_and_one_coverage.json",
        0.545454,
        "js",
    ),
    (
        interpret_test_coverage,
        "tests/unit/data/zero_cyclomatic_complexity.json",
        1.0,
        "js",
    ),
    (
        interpret_test_coverage,
        "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-CLI-04-13-2022-02-13-37-v1.1.1.json",
        0.5700000000000001,
        "py",
    ),
    (
        interpret_test_coverage,
        "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-Service-04-12-2022-17-32-35-v1.1.0.json",
        0.752962962962963,
        "py",
    ),
    (
        passed_tests,
        "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-CLI-04-13-2022-02-13-37-v1.1.1.json",
        1.0,
        "py",
    ),
    (
        passed_tests,
        "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-Service-04-12-2022-17-32-35-v1.1.0.json",
        0.7142857142857143,
        "py",
    ),
    (
        fast_test_builds,
        "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-CLI-04-13-2022-02-13-37-v1.1.1.json",
        0.00532,
        "py",
    ),
    (
        fast_test_builds,
        "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-Service-04-12-2022-17-32-35-v1.1.0.json",
        0.0010166666666666666,
        "py",
    ),
]

INVALID_ARGUMENTS_TEST_DATA = [
    (non_complex_files_density, None),
    (non_complex_files_density, False),
    (
        non_complex_files_density,
        pd.Series(data={"a": 1, "b": 2, "c": 3}, index=["a", "b", "c"]),
    ),
    (commented_files_density, None),
    (commented_files_density, False),
    (
        commented_files_density,
        pd.Series(data={"a": 1, "b": 2, "c": 3}, index=["a", "b", "c"]),
    ),
    (absence_of_duplications, None),
    (absence_of_duplications, False),
    (
        absence_of_duplications,
        pd.Series(data={"a": 1, "b": 2, "c": 3}, index=["a", "b", "c"]),
    ),
    (interpret_test_coverage, None),
    (interpret_test_coverage, False),
    (
        interpret_test_coverage,
        pd.Series(data={"a": 1, "b": 2, "c": 3}, index=["a", "b", "c"]),
    ),
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
