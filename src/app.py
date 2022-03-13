from flask import Flask
from flask_restful import Api
from src.resources.hello_world import HelloWorld

app = Flask(__name__)
api = Api(app)

api.add_resource(HelloWorld, "/hello")
