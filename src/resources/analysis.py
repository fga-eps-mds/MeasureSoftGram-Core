import random
import requests

from flask_restful import Resource
from flask import jsonify, request

from src.core.dataframe import create_dataframe
from src.core.analysis import calculate_measures, make_analysis
from src.util.exceptions import MeasureSoftGramCoreException
from src.util.constants import MEASURES_INTERPRETATION_MAPPING
from src.core.schemas import CalculateMeasureSchema

from marshmallow.exceptions import ValidationError


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
    """
    Recurso mockado
    TODO: Implementar
    """
    def post(self):
        return jsonify({
            "subcharacteristics": [
                {
                    "key": "testing_status",
                    "value": random.random()
                },
                {
                    "key": "modifiability",
                    "value": random.random()
                }
            ]
        })


class CalculateCharacteristics(Resource):
    """
    Recurso mockado
    TODO: Implementar
    """
    def post(self):
        return jsonify({
            "characteristics": [
                {
                    "key": "maintainability",
                    "value": random.random(),
                },
                {
                    "key": "reliability",
                    "value": random.random(),
                }
            ]
        })
