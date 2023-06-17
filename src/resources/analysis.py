import requests
from marshmallow.exceptions import ValidationError

from core.schemas import (
    CalculateMeasureSchema,
    CalculateSubCharacteristicSchema,
    CalculateCharacteristicSchema,
    CalculateTSQMISchema,
)

from util.constants import MEASURES_INTERPRETATION_MAPPING
from core.transformations import calculate_aggregated_weighted_value
import numpy as np 

def calculate_measures(
    extracted_measures,
    config: dict = {
        "characteristics": [{"subcharacteristics": [{"measures": [{"key": ""}]}]}]
    },
):
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

        measures = [
            measure
            for characteristic in config["characteristics"]
            for subcharacteristic in characteristic["subcharacteristics"]
            for measure in subcharacteristic["measures"]
        ]

        threshold_config = {
            key: value
            for measure in measures
            for key, value in measure.items()
            if measure["key"] == measure_key
            and key in MEASURES_INTERPRETATION_MAPPING[measure_key]["thresholds"]
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
        
        vector_aggregated_normalized_measure = np.array([])
        vector_weight_aggregated_normalized_measure = np.array([])
        
        for measure in subcharacteristic["measures"]:
            np.append(vector_aggregated_normalized_measure,measure["value"])
            np.append(vector_weight_aggregated_normalized_measure,measure["weight"])

        aggregated_value = calculate_aggregated_weighted_value(
                            vector_aggregated_normalized_measure, 
                            vector_weight_aggregated_normalized_measure)

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

        vector_aggregated_normalized_subcharacteristics = np.array([])
        vector_weight_aggregated_normalized_subcharacteristics = np.array([])
        for subcharacteristics in characteristic["subcharacteristics"]:
            np.append(vector_aggregated_normalized_subcharacteristics,subcharacteristics["value"])
            np.append(vector_weight_aggregated_normalized_subcharacteristics,subcharacteristics["weight"])

        aggregated_value = calculate_aggregated_weighted_value(vector_aggregated_normalized_subcharacteristics, vector_weight_aggregated_normalized_subcharacteristics)

        response_data["characteristics"].append(
            {
                "key": characteristic_key,
                "value": aggregated_value,
            }
        )

    return response_data


def calculate_tsqmi(extracted_tsqmi):
    try:
        data = CalculateTSQMISchema().load(extracted_tsqmi)
    except ValidationError as error:
        return {
            "error": "Failed to validate request",
            "schema_errors": error.messages,
            "code": requests.codes.unprocessable_entity,
        }

    response_data = {"tsqmi": []}

    tsqmi = data["tsqmi"]
    tsqmi_key: str = tsqmi["key"]


    vector_aggregated_normalized_characteristics = np.array([])
    vector_weight_aggregated_normalized_characteristics = np.array([])
    for characteristic in tsqmi["characteristics"]:
        np.append(vector_aggregated_normalized_characteristics, characteristic["value"])
        np.append(vector_weight_aggregated_normalized_characteristics, characteristic["weight"])
        
    aggregated_value = calculate_aggregated_weighted_value(vector_aggregated_normalized_characteristics,
                                                           vector_weight_aggregated_normalized_characteristics)

    response_data["tsqmi"].append(
        {
            "key": tsqmi_key,
            "value": aggregated_value,
        }
    )

    return response_data
