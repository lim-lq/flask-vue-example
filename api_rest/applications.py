# coding=utf-8
"""
desc:   generic applications define
author: levi-lq
date:   2017-05-23

"""

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("api_rest.settings")
app.secret_key = "secret_pass"

api = Api(app)

db = SQLAlchemy(app)
