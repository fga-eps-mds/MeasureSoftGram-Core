import requests
from flask_restful import Resource
from flask import jsonify, request
from src.core.dataframe import create_dataframe
from src.core.analysis import calculate_measures, make_analysis
from src.util.exceptions import MeasureSoftGramCoreException


class Analysis(Resource):
    def post(self):
        data = request.get_json(force=True)

        pre_config = data["pre_config"]
        components = data["components"]

        measures = pre_config["measures"]

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
