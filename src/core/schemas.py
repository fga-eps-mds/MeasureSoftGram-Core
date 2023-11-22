from marshmallow import Schema, fields, validate

class MetricSchema(Schema):
    """
    {
        "key": "tests"
        "value": [10.0]
    }
    """
    key = fields.Str(required=True)
    value = fields.List(fields.Float (required=True))


class MeasureSchema(Schema):
    """
    {
        "key": "passed_tests",
        "metrics": [
            {
                "key": "tests",
                "value": [10.0]
            },
            {
                "key": "test_errors",
                "value": [3.0]
            },
            {
                "key": "test_failures",
                "value": [1.0]
            }
        ]
    }
    """

    key = fields.Str(required=True)
    metrics = fields.List(fields.Nested(MetricSchema), required=True)


class CalculateMeasureSchema(Schema):
    """
    {
        
    "measures": [
            {
                "key": "passed_tests",
                "metrics": [
                    {
                        "key": "tests",
                        "value": [10.0]
                    },
                    {
                        "key": "test_errors",
                        "value": [3.0]
                    },
                    {
                        "key": "test_failures",
                        "value": [1.0]
                    }
                ]
            },
            {
                "key": "test_builds",
                "metrics": [
                    {
                        "key": "test_execution_time",
                        "value": [8.0]
                    },
                    {
                        "key": "tests",
                        "value": [10.0]
                    }
                ]
            },
    }
    """

    measures = fields.List(fields.Nested(MeasureSchema), required=True)


class CalculatedSubEntitySchema(Schema):
    key = fields.Str(required=True)
    value = fields.Float(validate=validate.Range(min=0, max=1), required=True)
    weight = fields.Float(validate=validate.Range(min=0, max=100), required=True)


class SubCharacteristicSchema(Schema):
    key = fields.Str(required=True)
    measures = fields.List(fields.Nested(CalculatedSubEntitySchema), required=True)


class CalculateSubCharacteristicSchema(Schema):
    """
    {
        "subcharacteristics": [
            {
                "key": "testing_status",
                "measures": [
                    {
                        "key": "passed_tests",
                        "value": 1.0,
                        "weight": 33,
                    },
                    ...
                ]
            },
            ...
        ]
    }
    """

    subcharacteristics = fields.List(fields.Nested(SubCharacteristicSchema), required=True)


class CharacteristicSchema(Schema):
    key = fields.Str(required=True)
    subcharacteristics = fields.List(fields.Nested(CalculatedSubEntitySchema), required=True)


class CalculateCharacteristicSchema(Schema):
    """
    {
        "characteristics": [
            {
                "key": "reliability",
                "subcharacteristics": [
                    {
                        "key": "testing_status",
                        "value": 1.0,
                        "weight": 50,
                    },
                    ...
                ]
            },
            ...
        ]
    }
    """

    characteristics = fields.List(fields.Nested(CharacteristicSchema), required=True)


class TSQMISchema(Schema):
    key = fields.Str(required=True)
    characteristics = fields.List(fields.Nested(CalculatedSubEntitySchema), required=True)


class CalculateTSQMISchema(Schema):
    """
    {
        "tsqmi": {
            "key": "tsqmi",
            "characteristics": [
                {
                    "key": "reliability",
                    "value": 1.0,
                    "weight": 50,
                },
                ...
            ]
        }
    }
    """

    tsqmi = fields.Nested(TSQMISchema, required=True)


class NonComplexFileDensitySchema(Schema):
    metrics = fields.List(fields.Nested(MetricSchema), required=True)


class CommentedFileDensitySchema(Schema):
    metrics = fields.List(fields.Nested(MetricSchema), required=True)


class DuplicationAbsenceSchema(Schema):
    metrics = fields.List(fields.Nested(MetricSchema), required=True)


class PassedTestsSchema(Schema):
    metrics = fields.List(fields.Nested(MetricSchema), required=True)
    @staticmethod
    def validate_metrics(metrics):
        for metric in metrics:
            #As métricas test_failures e test_errors só podem ser representadas por um valor flutuante 
            if metric['key'] in ['test_failures', 'test_errors'] and len(metric['value']) != 1:
                raise ValueError(f"'{metric['key']}' deveria ter apenas um valor flutuante")




class TestBuildsSchema(Schema):
    metrics = fields.List(fields.Nested(MetricSchema), required=True)


class TestCoverageSchema(Schema):
    metrics = fields.List(fields.Nested(MetricSchema), required=True)

#Todo : Implementar métricas do tipo inteiro
class TeamThroughputSchema(Schema):
    """
    "key": "team_throughput",
    "function": calculate_em7
    """

    total_issues = fields.Int(required=True)
    resolved_issues = fields.Int(required=True)
