# coding=utf-8
"""
desc:   initial project

"""

import models
import views

from flask import g
from flask_cors import CORS
from flask_restful import Resource

from applications import app, api, db
from http_responses import HTTP_200_OK
from utils import register_route

# solve cros site problem
CORS(app)


@app.before_request
def before_request():
    g.db = db


class Index(Resource):
    def get(self):
        return HTTP_200_OK()


api.add_resource(Index, "/", endpoint="index")
# register views url
register_route(api, "/api/v1.0", views.url_patterns)
