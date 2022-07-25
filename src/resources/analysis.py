import requests
from flask_restful import Resource
from flask import jsonify, request
from src.core.dataframe import create_dataframe
from src.core.analysis import calculate_measures, make_analysis
from src.core.exceptions import MeasureSoftGramCoreException

from src.core.interpretation_functions import calculate_em4


class Analysis(Resource):
    def post(self):
        data = request.get_json(force=True)

        pre_config = data["pre_config"] # Outro json com base json da pre-config
        components = data["components"] # Outro json com base json do sonar (subcomponents)

        measures = pre_config["measures"] # lista de str com as métricas

        df = create_dataframe(
            measures, components["components"], components["language_extension"]
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


class CalculateSpecificMeasure(Resource):
    FUNCTION_MAP = {
        "passed_tests": calculate_em4,
    }

    # "/calculate-measure/<string:measure_name>",
    def post(self, measure_name):
        funcs = CalculateSpecificMeasure.FUNCTION_MAP

        if measure_name not in funcs:
            return {
                "error": f"Measure {measure_name} not found"
            }, requests.codes.not_found

        data = request.get_json(force=True)

        try:
            result = funcs[measure_name](data)
            return jsonify({measure_name: result})
        except Exception:
            return {
                "error": f"Failed to calculate measure {measure_name}"
            }, requests.codes.unprocessable_entity
