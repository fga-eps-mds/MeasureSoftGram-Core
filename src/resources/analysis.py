from flask_restful import Resource
from flask import jsonify
from flask import request
import requests


class Analysis(Resource):
    def post(self):
        metrics = request.get_json(force=true)
