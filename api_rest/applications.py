# coding=utf-8
"""
desc:   generic applications define
author: levi-lq
date:   2017-05-23

"""

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from celery import Celery, platforms

platforms.C_FORCE_ROOT = True


def make_celery(app):
    """
    desc:   注入celery到flask中

    """
    celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"],
                    backend=app.config["CELERY_BACKEND_URL"])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.from_object("api_rest.settings")
app.secret_key = "secret_pass"

app.config.update(
    CELERYD_PREFETCH_MULTIPLIER="1",
    CELERY_RESULT_SERIALIZER="json",
    CELERYD_MAX_TASKS_PER_CHILD="10"
)
celery_ins = make_celery(app)

api = Api(app)

db = SQLAlchemy(app)

