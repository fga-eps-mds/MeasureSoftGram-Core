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


class PassedTestsSchema(Schema):
    tests = fields.Float(required=True)
    test_errors = fields.Float(required=True)
    test_failures = fields.Float(required=True)


class TestBuildsSchema(Schema):
    test_execution_time = fields.Float(required=True)


class TestCoverageSchema(Schema):
    number_of_files = fields.Integer(required=True)
    coverage = fields.List(fields.Float(required=True))


class NonComplexFileDensitySchema(Schema):
    complexity = fields.List(fields.Float(required=True))
    functions = fields.List(fields.Float(required=True))
    number_of_files = fields.Integer(required=True)


class CommentedFileDensitySchema(Schema):
    number_of_files = fields.Integer(required=True)
    comment_lines_density = fields.List(fields.Float(required=True))


class DuplicationAbsenceSchema(Schema):
    number_of_files = fields.Integer(required=True)
    duplicated_lines_density = fields.List(fields.Float(required=True))


class CIFeedbackTimeSchema(Schema):
    number_of_build_pipelines_in_the_last_x_days = fields.Integer(required=True)
    runtime_sum_of_build_pipelines_in_the_last_x_days = fields.Float(required=True)


class TeamThroughputSchema(Schema):
    number_of_resolved_issues = fields.Integer(required=True)
    total_number_of_issues = fields.Integer(required=True)
