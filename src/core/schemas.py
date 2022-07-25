from marshmallow import Schema, fields


class PassedTestsSchema(Schema):
    tests = fields.Float(required=True)
    test_errors = fields.Float(required=True)
    test_failures = fields.Float(required=True)
