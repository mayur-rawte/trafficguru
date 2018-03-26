from flask import Flask
from flask_restful import Resource, Api

from app.api import TraffiGuruAPI

app = Flask(__name__)
api = Api(app)

api.add_resource(TraffiGuruAPI, '/')

if __name__ == '__main__':
    app.run(debug=True)
