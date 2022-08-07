from marshmallow import Schema, fields


class MeasureSchema(Schema):
    """
    {
        "key": "passed_tests",
        "parameters": {
            "tests": 10,
            "test_errors": 3,
            "test_failures": 1
        }
    }
    """
    key = fields.Str(required=True)
    parameters = fields.Dict(required=True)


class CalculateMeasureSchema(Schema):
    """
    {
        "measures": [
            {
                "key": "passed_tests",
                "parameters": {
                    "tests": 10,
                    "test_errors": 3,
                    "test_failures": 1
                }
            },
            {
                "key": "test_builds",
                "parameters": {
                    "param1": 8,
                    "param2": 19,
                    "parma3": 4
                }
            }
        ]
    }
    """
    measures = fields.List(fields.Nested(MeasureSchema), required=True)


class NonComplexFileDensitySchema(Schema):
    """
    "key": "non_complex_file_density",
    "function": calculate_em1
    """
    complexity = fields.List(fields.Float(required=True))
    functions = fields.List(fields.Float(required=True))


class CommentedFileDensitySchema(Schema):
    """
    "key": "commented_file_density",
    "function": calculate_em2
    """
    comment_lines_density = fields.List(fields.Float(required=True))


class DuplicationAbsenceSchema(Schema):
    """
    "key": "duplication_absense",
    "function": calculate_em3
    """
    number_of_files = fields.Integer(required=True)
    duplicated_lines_density = fields.List(fields.Float(required=True))


class PassedTestsSchema(Schema):
    """
    "key": "passed_tests",
    "function": calculate_em4
    """
    tests = fields.Float(required=True)
    test_errors = fields.Float(required=True)
    test_failures = fields.Float(required=True)


class TestBuildsSchema(Schema):
    """
    "key": "test_builds",
    "function": calculate_em5
    """
    test_execution_time = fields.Float(required=True)


class TestCoverageSchema(Schema):
    """
    "key": "test_coverage",
    "function": calculate_em6
    """
    number_of_files = fields.Integer(required=True)
    coverage = fields.List(fields.Float(required=True))


class TeamThroughputSchema(Schema):
    """
    "key": "team_throughput",
    "function": calculate_em7
    """
    number_of_resolved_issues_in_the_last_x_days = fields.Integer(required=True)
    total_number_of_issues_in_the_last_x_days = fields.Integer(required=True)


class CIFeedbackTimeSchema(Schema):
    """
    "key": "ci_feedback_time",
    "function": calculate_em8
    """
    number_of_build_pipelines_in_the_last_x_days = fields.Integer(required=True)
    runtime_sum_of_build_pipelines_in_the_last_x_days = fields.Float(required=True)
