from marshmallow import Schema, fields


class PassedTestsSchema(Schema):
    tests = fields.Float(required=True)
    test_errors = fields.Float(required=True)
    test_failures = fields.Float(required=True)


class TestBuildsSchema(Schema):
    test_execution_time = fields.Float(required=True)


class TestCoverageSchema(Schema):
    coverage = fields.Float(required=True)


class NonComplexFileDensitySchema(Schema):
    complexity = fields.Float(required=True)
    functions = fields.Float(required=True)


class CommentedFileDensitySchema(Schema):
    comment_lines_density = fields.Float(required=True)


class DuplicationAbsenceSchema(Schema):
    duplicated_lines_density = fields.Float(required=True)
