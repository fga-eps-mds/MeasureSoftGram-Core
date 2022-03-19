from flask import Flask
from flask_restful import Api
from src.resources.hello_world import HelloWorld
from src.resources.available import AvailablePreConfigs

app = Flask(__name__)
api = Api(app)

api.add_resource(HelloWorld, "/hello")

api.add_resource(AvailablePreConfigs, "/available-pre-configs")
