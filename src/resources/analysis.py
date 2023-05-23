import requests
from marshmallow.exceptions import ValidationError

from core.schemas import (
    CalculateMeasureSchema,
    CalculateSubCharacteristicSchema,
    CalculateCharacteristicSchema,
    CalculateSQCSchema,
)
from core.agregation import aggregation_operation
from core.weighting import weighting_operation
from util.constants import MEASURES_INTERPRETATION_MAPPING


def calculate_aggregated_value(values_list, weights_list):
    weighted_items = weighting_operation(values_list, weights_list)
    return aggregation_operation(weighted_items, weights_list)


def calculate_measures(extracted_measures, config: dict = {"thresholds": {}}):
    # Validate if outter keys is valid
    try:
        data = CalculateMeasureSchema().load(extracted_measures)
    except ValidationError as error:
        return {
            "error": "Failed to validate request",
            "schema_errors": error.messages,
            "code": requests.codes.unprocessable_entity,
        }

    # Objeto retornado em caso de sucesso
    response_data = {"measures": []}

    valid_measures = MEASURES_INTERPRETATION_MAPPING.keys()

    for measure in data["measures"]:
        measure_key: str = measure["key"]

        if measure_key not in valid_measures:
            return {
                "error": f"Measure {measure_key} is not supported",
                "code": requests.codes.unprocessable_entity,
            }

        measure_params = measure["parameters"]
        schema = MEASURES_INTERPRETATION_MAPPING[measure_key]["schema"]

        try:
            validated_params = schema().load(measure_params)
        except ValidationError as exc:
            return {
                "error": f"Metric parameters {measure_key} are not valid",
                "schema_errors": exc.messages,
                "code": requests.codes.unprocessable_entity,
            }

        interpretation_function = MEASURES_INTERPRETATION_MAPPING[measure_key][
            "interpretation_function"
        ]
        threshold_config = {
            threshold: config["thresholds"][threshold]
            for threshold in config["thresholds"].keys()
            if threshold in MEASURES_INTERPRETATION_MAPPING[measure_key]["thresholds"]
        }
        result = interpretation_function(validated_params, **threshold_config)

        response_data["measures"].append(
            {
                "key": measure_key,
                "value": result,
            }
        )

    return response_data


def calculate_subcharacteristics(extracted_subcharacteristics):
    try:
        data = CalculateSubCharacteristicSchema().load(extracted_subcharacteristics)
    except ValidationError as error:
        return {
            "error": "Failed to validate request",
            "schema_errors": error.messages,
            "code": requests.codes.unprocessable_entity,
        }

    response_data = {"subcharacteristics": []}

    for subcharacteristic in data["subcharacteristics"]:
        subcharacteristic_key: str = subcharacteristic["key"]

        values_list, weights_list = [], []
        for measure in subcharacteristic["measures"]:
            values_list.append(measure["value"])
            weights_list.append(measure["weight"])

        aggregated_value = calculate_aggregated_value(values_list, weights_list)

        response_data["subcharacteristics"].append(
            {
                "key": subcharacteristic_key,
                "value": aggregated_value,
            }
        )

    return response_data


def calculate_characteristics(extracted_characteristics):
    try:
        data = CalculateCharacteristicSchema().load(extracted_characteristics)
    except ValidationError as error:
        return {
            "error": "Failed to validate request",
            "schema_errors": error.messages,
            "code": requests.codes.unprocessable_entity,
        }

    response_data = {"characteristics": []}

    for characteristic in data["characteristics"]:
        characteristic_key: str = characteristic["key"]

        values_list, weights_list = [], []
        for measure in characteristic["subcharacteristics"]:
            values_list.append(measure["value"])
            weights_list.append(measure["weight"])

        aggregated_value = calculate_aggregated_value(values_list, weights_list)

        response_data["characteristics"].append(
            {
                "key": characteristic_key,
                "value": aggregated_value,
            }
        )

    return response_data


def calculate_sqc(extracted_sqc):
    try:
        data = CalculateSQCSchema().load(extracted_sqc)
    except ValidationError as error:
        return {
            "error": "Failed to validate request",
            "schema_errors": error.messages,
            "code": requests.codes.unprocessable_entity,
        }

    response_data = {"sqc": []}

    sqc = data["sqc"]
    sqc_key: str = sqc["key"]

    values_list, weights_list = [], []
    for characteristic in sqc["characteristics"]:
        values_list.append(characteristic["value"])
        weights_list.append(characteristic["weight"])

    aggregated_value = calculate_aggregated_value(values_list, weights_list)

    response_data["sqc"].append(
        {
            "key": sqc_key,
            "value": aggregated_value,
        }
    )

    return response_data
