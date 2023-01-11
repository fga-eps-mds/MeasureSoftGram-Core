from flask import Flask
from flask_restful import Api

from resources.analysis import (
    Analysis,
    CalculateCharacteristics,
    CalculateMeasures,
    CalculateSQC,
    CalculateSubcharacteristics,
)
from resources.available import AvailablePreConfigs

app = Flask(__name__)
api = Api(app)

api.add_resource(AvailablePreConfigs, "/available-pre-configs")

api.add_resource(Analysis, "/analysis")

api.add_resource(
    CalculateMeasures,
    "/calculate-measures/",
)

api.add_resource(
    CalculateSubcharacteristics,
    "/calculate-subcharacteristics/",
)

api.add_resource(
    CalculateCharacteristics,
    "/calculate-characteristics/",
)

api.add_resource(
    CalculateSQC,
    "/calculate-sqc/",
)
