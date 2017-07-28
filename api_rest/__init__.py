# coding=utf-8
"""
desc:   initial project

"""

from api_rest import models
from api_rest import views

from flask import g
from flask_cors import CORS
from flask_restful import Resource

from api_rest.applications import app, api, db, redis_cache
from api_rest.http_responses import HTTP_200_OK
from api_rest.utils import register_route

# solve cros site problem
CORS(app)


@app.before_request
def before_request():
    g.db = db
    g.cache = redis_cache


class Index(Resource):
    def get(self):
        return HTTP_200_OK()


api.add_resource(Index, "/", endpoint="index")
# register views url
register_route(api, "/api/v1.0", views.url_patterns)
