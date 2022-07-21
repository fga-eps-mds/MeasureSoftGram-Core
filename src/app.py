from flask import Flask
from flask_restful import Api
from src.resources.available import AvailablePreConfigs
from src.resources.analysis import (
    Analysis,
    CalculateSpecificMeasure,
)


app = Flask(__name__)
api = Api(app)

api.add_resource(AvailablePreConfigs, "/available-pre-configs")

api.add_resource(Analysis, "/analysis")

api.add_resource(
    CalculateSpecificMeasure,
    "/calculate-measure/<string:measure_name>",
)
