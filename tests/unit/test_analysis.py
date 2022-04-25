from src.core.analysis import calculate_measures
from src.core.analysis import resolve_level
from src.core.analysis import make_analysis
from tests.test_helpers import create_file_df
import pytest

json_list_1 = [
    "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-Service-04-12-2022-17-32-35-v1.1.0.json"
]


def test_calculate_measures():
    data_frame_1 = create_file_df(
        json_list_1,
        "py",
    )

    measures = [
        "test_builds",
        "test_coverage",
        "passed_tests",
    ]

    expected_measures = {
        "test_builds": 0.0010166666666666666,
        "test_coverage": 0.5647222222222222,
        "passed_tests": 0.7142857142857143,
    }

    combined_measures = calculate_measures(data_frame_1, measures)
    assert (
        pytest.approx(combined_measures["test_builds"]) == expected_measures["test_builds"]
    )
    assert (
        pytest.approx(combined_measures["test_coverage"]) == expected_measures["test_coverage"]
    )
    assert (
        pytest.approx(combined_measures["passed_tests"]) == expected_measures["passed_tests"]
    )

    return


characteristics1 = {
    "reliability": {
        "weight": 1.0,
        "subcharacteristics": ["testing_status"],
        "weights": {"testing_status": 1.0},
    },
}

subcharacteristics1 = {
    "testing_status": {
        "measures": ["test_builds", "test_coverage", "passed_tests"],
        "weights": {
            "test_builds": 0.3333,
            "test_coverage": 0.3333,
            "passed_tests": 0.3333,
        },
    }
}

measures1 = {
    "test_builds": 0.0010166666666666666,
    "test_coverage": 0.5647222222222222,
    "passed_tests": 0.7142857142857143,
}


def test_resolve_level():
    aggregate_level = resolve_level(subcharacteristics1, measures1, "measures")

    assert pytest.approx(aggregate_level["testing_status"]) == 0.525711


def test_make_analysis():
    sqc, agregated_sbc, aggregated_characteristics = make_analysis(
        measures1, subcharacteristics1, characteristics1
    )
    assert pytest.approx(agregated_sbc["testing_status"]) == 0.525711
    assert pytest.approx(aggregated_characteristics["reliability"]) == 0.525711
    assert pytest.approx(sqc["sqc"]) == 0.525711
