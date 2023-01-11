import requests
from flask import jsonify, request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError

from core.analysis import (
    calculate_aggregated_value,
    calculate_measures,
    make_analysis,
    calculate_sqc,
)
from core.dataframe import create_dataframe
from core.schemas import (
    CalculateMeasureSchema,
    CalculateSubCharacteristicSchema,
    CalculateCharacteristicSchema,
    CalculateSQCSchema,
)
from util.constants import MEASURES_INTERPRETATION_MAPPING
from util.exceptions import MeasureSoftGramCoreException


class Analysis(Resource):
    def post(self):
        data = request.get_json(force=True)

        pre_config = data["pre_config"]
        components = data["components"]
        measures = pre_config["measures"]

        df = create_dataframe(
            measures,
            components["components"],
            components["language_extension"],
        )

        try:
            aggregated_measures = calculate_measures(df, measures)
        except MeasureSoftGramCoreException as error:
            return {
                "error": f"Failed to calculate measures: {error}"
            }, requests.codes.unprocessable_entity

        (
            sqc_analysis,
            aggregated_scs,
            aggregated_characteristics,
            weighted_measures_per_scs,
            weighted_scs_per_c,
            weighted_c,
        ) = make_analysis(
            aggregated_measures,
            pre_config["subcharacteristics"],
            pre_config["characteristics"],
        )

        return jsonify(
            {
                "sqc": sqc_analysis,
                "subcharacteristics": aggregated_scs,
                "characteristics": aggregated_characteristics,
                "weighted_measures": weighted_measures_per_scs,
                "weighted_subcharacteristics": weighted_scs_per_c,
                "weighted_characteristics": weighted_c,
            }
        )


class CalculateMeasures(Resource):
    def post(self):
        # Validate if outter keys is valid
        try:
            data = CalculateMeasureSchema().load(request.get_json(force=True))
        except ValidationError as error:
            return {
                "error": "Failed to validate request",
                "schema_errors": error.messages,
            }, requests.codes.unprocessable_entity

        # Objeto retornado em caso de sucesso
        response_data = {"measures": []}

        valid_measures = MEASURES_INTERPRETATION_MAPPING.keys()

        for measure in data["measures"]:
            measure_key: str = measure['key']

            if measure_key not in valid_measures:
                return {
                    "error": f"Measure {measure_key} is not supported",
                }, requests.codes.unprocessable_entity

            measure_params = measure["parameters"]
            schema = MEASURES_INTERPRETATION_MAPPING[measure_key]["schema"]

            try:
                validated_params = schema().load(measure_params)
            except ValidationError as exc:
                return {
                    "error": {
                        "message": f"Metric parameters `{measure_key}` are not valid",
                        "schema_errors": exc.messages,
                    }
                }, requests.codes.unprocessable_entity

            interpretation_function = MEASURES_INTERPRETATION_MAPPING[measure_key]["calculation_function"]
            result = interpretation_function(validated_params)

            response_data["measures"].append({
                "key": measure_key,
                "value": result,
            })

        return jsonify(response_data)


class CalculateSubcharacteristics(Resource):
    def post(self):
        # Validates if the request data is valid
        try:
            data = CalculateSubCharacteristicSchema().load(request.get_json(force=True))
        except ValidationError as error:
            return {
                "error": "Failed to validate request",
                "schema_errors": error.messages,
            }, requests.codes.unprocessable_entity

        response_data = {"subcharacteristics": []}

        for subcharacteristic in data["subcharacteristics"]:
            subcharacteristic_key: str = subcharacteristic["key"]

            values_list, weights_list = [], []
            for measure in subcharacteristic["measures"]:
                values_list.append(measure["value"])
                weights_list.append(measure["weight"])

            aggregated_value = calculate_aggregated_value(values_list, weights_list)

            response_data["subcharacteristics"].append({
                "key": subcharacteristic_key,
                "value": aggregated_value,
            })

        return jsonify(response_data)


class CalculateCharacteristics(Resource):
    def post(self):
        # Validate if the request data is valid
        try:
            data = CalculateCharacteristicSchema().load(request.get_json(force=True))
        except ValidationError as error:
            return {
                "error": "Failed to validate request",
                "schema_errors": error.messages,
            }, requests.codes.unprocessable_entity

        response_data = {"characteristics": []}

        for characteristic in data["characteristics"]:
            characteristic_key: str = characteristic["key"]

            values_list, weights_list = [], []
            for measure in characteristic["subcharacteristics"]:
                values_list.append(measure["value"])
                weights_list.append(measure["weight"])

            aggregated_value = calculate_aggregated_value(values_list, weights_list)

            response_data["characteristics"].append({
                "key": characteristic_key,
                "value": aggregated_value,
            })

        return jsonify(response_data)


class CalculateSQC(Resource):
    def post(self):
        # Validate if the request data is valid
        try:
            data = CalculateSQCSchema().load(request.get_json(force=True))
        except ValidationError as error:
            return {
                "error": "Failed to validate request",
                "schema_errors": error.messages,
            }, requests.codes.unprocessable_entity

        sqc = calculate_sqc(data["pre_config"], data["metrics"])

        return jsonify({
            "value": sqc,
        })
