# coding=utf-8
"""
desc:   错误处理handler
author: congqing.li
date:   2016-10-28

"""
from werkzeug.exceptions import HTTPException


class CustomError(HTTPException):
    code = None
    description = "NIMABI"

    def __init__(self, description=None, response=None):
        if isinstance(description, tuple):
            self.description, self.code = description


class ObjectNotExists(CustomError):
    pass


class TokenExpired(CustomError):
    pass


class BadToken(CustomError):
    pass


class MissToken(CustomError):
    pass


class Forbidden(CustomError):
    pass


class BadRequest(CustomError):
    pass


class UpdateError(CustomError):
    pass
