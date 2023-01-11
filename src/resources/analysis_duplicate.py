import requests
from marshmallow.exceptions import ValidationError

from core.schemas import (
    CalculateMeasureSchema
)
from util.constants import MEASURES_INTERPRETATION_MAPPING


def calculate_measures(extracted_measures):
    # Validate if outter keys is valid
    try:
        data = CalculateMeasureSchema().load(extracted_measures)
    except ValidationError as error:
        return {
            "error": "Failed to validate request",
            "schema_errors": error.messages,
            "code": requests.codes.unprocessable_entity
        }

    # Objeto retornado em caso de sucesso
    response_data = {"measures": []}

    valid_measures = MEASURES_INTERPRETATION_MAPPING.keys()

    for measure in data["measures"]:
        measure_key: str = measure['key']

        if measure_key not in valid_measures:
            return {
                "error": f"Measure {measure_key} is not supported",
                "code": requests.codes.unprocessable_entity
            }

        measure_params = measure["parameters"]
        schema = MEASURES_INTERPRETATION_MAPPING[measure_key]["schema"]

        try:
            validated_params = schema().load(measure_params)
        except ValidationError as exc:
            return {
                "error": {
                    "message": f"Metric parameters `{measure_key}` are not valid",
                    "schema_errors": exc.messages,
                    "code": requests.codes.unprocessable_entity
                }
            }

        interpretation_function = MEASURES_INTERPRETATION_MAPPING[measure_key]["calculation_function"]
        result = interpretation_function(validated_params)

        response_data["measures"].append({
            "key": measure_key,
            "value": result,
        })

    return response_data
