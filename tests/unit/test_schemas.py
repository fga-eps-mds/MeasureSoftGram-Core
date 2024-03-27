import pytest
from marshmallow.exceptions import ValidationError

from core.schemas import (
    NonComplexFileDensitySchema,
    CommentedFileDensitySchema,
    DuplicationAbsenceSchema,
    PassedTestsSchema,
    TestBuildsSchema,
    TestCoverageSchema,
    CIFeedbackTimeSchema,
    TeamThroughputSchema,
)

from tests.utils.schemas_data import (
    NON_COMPLEX_FILES_DENSITY_METRICS_DATA,
    COMMENTED_FILE_DENSITY_METRICS_DATA,
    DUPLICATION_ABSENCE_METRICS_DATA,
    PASSED_TESTS_METRICS_DATA,
    TEST_BUILDS_METRICS_DATA,
    TEST_COVERAGE_METRICS_DATA,
    CI_FEEDBACK_TIME_METRICS_DATA,
    TEAM_THROUGHPUT_METRICS_DATA,
)


def test_non_complex_file_density_schema_validation():
    try:
        NonComplexFileDensitySchema().load(NON_COMPLEX_FILES_DENSITY_METRICS_DATA)
    except ValidationError as e:
        pytest.fail(f"Unexpected error: {e}")


def test_commented_file_density_schema_validation():
    try:
        CommentedFileDensitySchema().load(COMMENTED_FILE_DENSITY_METRICS_DATA)
    except ValidationError as e:
        pytest.fail(f"Unexpected error: {e}")


def test_duplication_absence_schema_validation():
    try:
        DuplicationAbsenceSchema().load(DUPLICATION_ABSENCE_METRICS_DATA)
    except ValidationError as e:
        pytest.fail(f"Unexpected error: {e}")


def test_passed_tests_schema_validation():
    try:
        PassedTestsSchema().load(PASSED_TESTS_METRICS_DATA)
    except ValidationError as e:
        pytest.fail(f"Unexpected error: {e}")


def test_test_builds_schema_validation():
    try:
        TestBuildsSchema().load(TEST_BUILDS_METRICS_DATA)
    except ValidationError as e:
        pytest.fail(f"Unexpected error: {e}")


def test_test_coverage_schema_validation():
    try:
        TestCoverageSchema().load(TEST_COVERAGE_METRICS_DATA)
    except ValidationError as e:
        pytest.fail(f"Unexpected error: {e}")


def test_ci_feedback_time_schema_validation():
    try:
        CIFeedbackTimeSchema().load(CI_FEEDBACK_TIME_METRICS_DATA)
    except ValidationError as e:
        pytest.fail(f"Unexpected error: {e}")


def test_team_throughput_schema_validation():
    try:
        TeamThroughputSchema().load(TEAM_THROUGHPUT_METRICS_DATA)
    except ValidationError as e:
        pytest.fail(f"Unexpected error: {e}")
