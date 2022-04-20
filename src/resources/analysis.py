from flask_restful import Resource
<<<<<<< HEAD
from flask import jsonify, request
from src.core.constants import AVAILABLE_PRE_CONFIGS
from src.core.dataframe import create_dataframe
from src.core.analysis import calculate_measures, make_analysis
=======
from flask import jsonify
from src.core.constants import AVAILABLE_PRE_CONFIGS
>>>>>>> 450cdd219e70c6d91e08ef9216ac8907e06e20bb


class Analysis(Resource):
    def post(self):
<<<<<<< HEAD
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
=======
        return jsonify(AVAILABLE_PRE_CONFIGS)
>>>>>>> 450cdd219e70c6d91e08ef9216ac8907e06e20bb
