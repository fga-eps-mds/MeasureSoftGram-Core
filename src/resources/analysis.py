import numpy as np
from marshmallow.exceptions import ValidationError

from core.schemas import (
    CalculateCharacteristicSchema,
    CalculateMeasureSchema,
    CalculateSubCharacteristicSchema,
    CalculateTSQMISchema,
)
from core.transformations import calculate_aggregated_weighted_value
from util.constants import AGGREGATED_NORMALIZED_MEASURES_MAPPING
from util.exceptions import MeasureKeyNotSupported


def calculate_measures(
    extracted_measures: CalculateMeasureSchema,
    config: dict = {
        "characteristics": [{"subcharacteristics": [{"measures": [{"key": ""}]}]}]
    },
):
    # Validate if outter keys is valid
    try:
        data = CalculateMeasureSchema().load(extracted_measures)
    except ValidationError as error:
        raise ValidationError(
            f"error: Failed to validate input.\nschema_errors: {error.messages}"
        )

    # Objeto retornado em caso de sucesso
    result_data = {"measures": []}

    valid_measures = AGGREGATED_NORMALIZED_MEASURES_MAPPING.keys()

    for measure in data["measures"]:
        measure_key: str = measure["key"]

        if measure_key not in valid_measures:
            raise MeasureKeyNotSupported(f"Measure {measure_key} is not supported")

        measure_params = measure["parameters"]
        schema = AGGREGATED_NORMALIZED_MEASURES_MAPPING[measure_key]["schema"]

        try:
            validated_params = schema().load(measure_params)
        except ValidationError as exc:
            raise ValidationError(
                f"error: Metric parameters {measure_key} are not valid.\nschema_errors: {exc.messages}"
            )

        aggregated_normalized_measure = AGGREGATED_NORMALIZED_MEASURES_MAPPING[
            measure_key
        ]["aggregated_normalized_measure"]

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
            and key in AGGREGATED_NORMALIZED_MEASURES_MAPPING[measure_key]["thresholds"]
        }

        result = aggregated_normalized_measure(validated_params, **threshold_config)

        result_data["measures"].append(
            {
                "key": measure_key,
                "value": result,
            }
        )

    return result_data


def calculate_subcharacteristics(extracted_subcharacteristics):
    try:
        data = CalculateSubCharacteristicSchema().load(extracted_subcharacteristics)
    except ValidationError as error:
        raise ValidationError(
            f"error: Failed to validate input.\nschema_errors: {error.messages}"
        )

    result_data = {"subcharacteristics": []}

    for subcharacteristic in data["subcharacteristics"]:
        subcharacteristic_key: str = subcharacteristic["key"]

        vector_aggregated_normalized_measure = np.array([])
        vector_weight_aggregated_normalized_measure = np.array([])

        for measure in subcharacteristic["measures"]:
            vector_aggregated_normalized_measure = np.append(
                vector_aggregated_normalized_measure, measure["value"]
            )
            vector_weight_aggregated_normalized_measure = np.append(
                vector_weight_aggregated_normalized_measure, measure["weight"]
            )
        aggregated_value = calculate_aggregated_weighted_value(
            vector_aggregated_normalized_measure,
            vector_weight_aggregated_normalized_measure,
        )

        result_data["subcharacteristics"].append(
            {
                "key": subcharacteristic_key,
                "value": aggregated_value,
            }
        )

    return result_data


def calculate_characteristics(extracted_characteristics):
    try:
        data = CalculateCharacteristicSchema().load(extracted_characteristics)
    except ValidationError as error:
        raise ValidationError(
            f"error: Failed to validate input.\nschema_errors: {error.messages}"
        )

    result_data = {"characteristics": []}

    for characteristic in data["characteristics"]:
        characteristic_key: str = characteristic["key"]

        vector_aggregated_normalized_subcharacteristics = np.array([])
        vector_weight_aggregated_normalized_subcharacteristics = np.array([])
        for subcharacteristics in characteristic["subcharacteristics"]:
            vector_aggregated_normalized_subcharacteristics = np.append(
                vector_aggregated_normalized_subcharacteristics,
                subcharacteristics["value"],
            )
            vector_weight_aggregated_normalized_subcharacteristics = np.append(
                vector_weight_aggregated_normalized_subcharacteristics,
                subcharacteristics["weight"],
            )

        aggregated_value = calculate_aggregated_weighted_value(
            vector_aggregated_normalized_subcharacteristics,
            vector_weight_aggregated_normalized_subcharacteristics,
        )

        result_data["characteristics"].append(
            {
                "key": characteristic_key,
                "value": aggregated_value,
            }
        )

    return result_data


def calculate_tsqmi(extracted_tsqmi):
    try:
        data = CalculateTSQMISchema().load(extracted_tsqmi)
    except ValidationError as error:
        raise ValidationError(
            f"error: Failed to validate input.\nschema_errors: {error.messages}"
        )

    result_data = {"tsqmi": []}

    tsqmi = data["tsqmi"]
    tsqmi_key: str = tsqmi["key"]

    vector_aggregated_normalized_characteristics = np.array([])
    vector_weight_aggregated_normalized_characteristics = np.array([])
    for characteristic in tsqmi["characteristics"]:
        vector_aggregated_normalized_characteristics = np.append(
            vector_aggregated_normalized_characteristics, characteristic["value"]
        )
        vector_weight_aggregated_normalized_characteristics = np.append(
            vector_weight_aggregated_normalized_characteristics,
            characteristic["weight"],
        )

    aggregated_value = calculate_aggregated_weighted_value(
        vector_aggregated_normalized_characteristics,
        vector_weight_aggregated_normalized_characteristics,
    )

    result_data["tsqmi"].append(
        {
            "key": tsqmi_key,
            "value": aggregated_value,
        }
    )

    return result_data
