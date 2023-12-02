from marshmallow import Schema, fields, validate
from marshmallow.exceptions import ValidationError


class MetricSchema(Schema):
    """
    {
        "key": "tests"
        "value": [10.0]
    }
    """

    key = fields.Str(required=True)
    value = fields.List(fields.Float(required=True))


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

    subcharacteristics = fields.List(
        fields.Nested(SubCharacteristicSchema), required=True
    )


class CharacteristicSchema(Schema):
    key = fields.Str(required=True)
    subcharacteristics = fields.List(
        fields.Nested(CalculatedSubEntitySchema), required=True
    )


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
    characteristics = fields.List(
        fields.Nested(CalculatedSubEntitySchema), required=True
    )


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
    # 1 Validação : Se contém uma lista de métricas
    metrics = fields.List(fields.Nested(MetricSchema), required=True)

    @staticmethod
    def validate_metrics(metrics):
        for metric in metrics:
            # 2 Validação : Se foi passada alguma métrica não pertencente a medida
            if metric["key"] not in ["complexity", "functions"]:
                raise ValidationError(
                    f"'{metric['key']}': Métrica não presente na medida"
                )


class CommentedFileDensitySchema(Schema):
    # 1 Validação : Se contém uma lista de métricas
    metrics = fields.List(fields.Nested(MetricSchema), required=True)

    @staticmethod
    def validate_metrics(metrics):
        for metric in metrics:
            # 2 Validação : Se foi passada alguma métrica não pertencente a medida
            if metric["key"] not in ["comment_lines_density"]:
                raise ValidationError(
                    f"'{metric['key']}': Métrica não presente na medida"
                )


class DuplicationAbsenceSchema(Schema):
    # 1 Validação : Se contém uma lista de métricas
    metrics = fields.List(fields.Nested(MetricSchema), required=True)

    @staticmethod
    def validate_metrics(metrics):
        for metric in metrics:
            # 2 Validação : Se foi passada alguma métrica não pertencente a medida
            if metric["key"] not in ["duplicated_lines_density"]:
                raise ValidationError(
                    f"'{metric['key']}': Métrica não presente na medida"
                )


class PassedTestsSchema(Schema):
    # 1 Validação : Se contém uma lista de métricas
    metrics = fields.List(fields.Nested(MetricSchema), required=True)

    @staticmethod
    def validate_metrics(metrics):
        for metric in metrics:
            # 2 Validação : Se foi passada alguma métrica não pertencente a medida
            if metric["key"] not in ["tests", "test_failures", "test_errors"]:
                raise ValidationError(
                    f"'{metric['key']}': Métrica não presente na medida"
                )

            # 3 Validação: As métricas test_failures e test_errors só podem ser
            #             representadas por um array de um único elemento flutuante
            if metric["key"] in ["test_failures", "test_errors"]:
                if len(metric["value"]) != 1:
                    raise ValidationError(
                        f"'{metric['key']}': Deveria ser um array de um único valor"
                    )
                if not isinstance(metric["value"][0], float):
                    raise ValidationError(
                        f"'{metric['key']}': Deveria ser um valor flutuante"
                    )


class TestBuildsSchema(Schema):
    # 1 Validação : Se contém uma lista de métricas
    metrics = fields.List(fields.Nested(MetricSchema), required=True)

    @staticmethod
    def validate_metrics(metrics):
        for metric in metrics:
            # 2 Validação : Se foi passada alguma métrica não pertencente a medida
            if metric["key"] not in ["test_execution_time", "tests"]:
                raise ValidationError(
                    f"'{metric['key']}': Métrica não presente na medida"
                )


class TestCoverageSchema(Schema):
    # 1 Validação : Se contém uma lista de métricas
    metrics = fields.List(fields.Nested(MetricSchema), required=True)

    @staticmethod
    def validate_metrics(metrics):
        for metric in metrics:
            # 2 Validação : Se foi passada alguma métrica não pertencente a medida
            if metric["key"] not in ["coverage"]:
                raise ValidationError(
                    f"'{metric['key']}': Métrica não presente na medida"
                )


class TeamThroughputSchema(Schema):
    # 1 Validação : Se contém uma lista de métricas
    metrics = fields.List(fields.Nested(MetricSchema), required=True)

    @staticmethod
    def validate_metrics(metrics):
        for metric in metrics:
            # 2 Validação : Se foi passada alguma métrica não pertencente a medida
            if metric["key"] not in ["resolved_issues", "total_issues"]:
                raise ValidationError(
                    f"'{metric['key']}': Métrica não presente na medida"
                )

            # 3 Validação: As métricas só podem ser representadas por um array de
            #             um único elemento inteiro
            if len(metric["value"]) != 1:
                raise ValidationError(
                    f"'{metric['key']}': Deveria ser um array de um único valor"
                )
            if not isinstance(metric["value"][0], float):
                raise ValidationError(
                    f"'{metric['key']}': Deveria ser um valor flutuante"
                )
