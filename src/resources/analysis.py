from flask_restful import Resource
from flask import jsonify, request
from src.core.constants import AVAILABLE_PRE_CONFIGS
from src.core.dataframe import create_dataframe
from src.core.analysis import calculate_measures, make_analysis


class Analysis(Resource):
    def post(self):
        data = request.get_json(force=True)

        pre_config = data["pre_config"]
        components = data["components"]

        metrics = list(pre_config["metrics"].keys())

        df = create_dataframe(metrics, components, pre_config["language_extension"])

        aggregated_measures = calculate_measures(df, metrics)

        sqc_analysis = make_analysis(
            aggregated_measures,
            pre_config["subcharacteristics"],
            pre_config["characteristics"],
        )

        return jsonify({"sqc": sqc_analysis})
