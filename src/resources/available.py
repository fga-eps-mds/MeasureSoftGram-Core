from flask import jsonify
from flask_restful import Resource

from util.constants import AVAILABLE_PRE_CONFIGS


class AvailablePreConfigs(Resource):
    def get(self):
        return jsonify(AVAILABLE_PRE_CONFIGS)
