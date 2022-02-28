from flask import jsonify
from flask_restful import Resource


class HelloWorld(Resource):
    def get(self):
        return jsonify({"Hello": "World!"})
