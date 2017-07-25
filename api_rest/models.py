# coding=utf-8
"""
desc:   database model define

"""

import datetime

from applications import db


class BaseModel(object):
    """
    desc:   基本模型数据
    Usage:  class User(BaseModel, db.Model):
                pass

    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    modify_date = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def _to_dict(self, **kwargs):
        """
        desc:   将数据转换为json格式的

        """
        json_data = {
            "id": self.id,
            "create_date": self.create_date.strftime("%Y-%m-%d %H:%M:%S"),
            "modify_date": self.modify_date.strftime("%Y-%m-%d %H:%M:%S")
        }
        for key, value in kwargs.iteritems():
            json_data[key] = value
        return json_data


class Students(BaseModel, db.Model):
    """
    desc:   学生表模型

    """
    name = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return self._to_dict(name=self.name)
