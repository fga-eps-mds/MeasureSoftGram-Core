from flask_restful import Resource
from flask import jsonify
from src.core.constants import AVAILABLE_PRE_CONFIGS


class Analysis(Resource):
    def post(self):
        return jsonify(AVAILABLE_PRE_CONFIGS)
