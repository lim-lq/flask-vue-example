# coding=utf-8
"""
desc:   flask_restful response to http code
Usage:  HTTP_200_OK() or HTTP_200_OK(msg=xxx)

"""

from functools import partial


def success(status_code, msg="OK"):
    return {
        "status": "success",
        "result": msg
    }, status_code


def failure(status_code, msg="error"):
    return {
        "status": "failure",
        "result": msg
    }, status_code


HTTP_200_OK = partial(success, 200, msg="OK")

HTTP_201_CREATED = partial(success, 201, msg="CREATED")

HTTP_400_BAD_REQUEST = partial(failure, 400, msg="Bad request")

HTTP_404_NOT_FOUND = partial(failure, 404, msg="Not Found")

HTTP_403_FORBIDDEN = partial(failure, 403, msg="Forbidden")

HTTP_500_INTERNAL_ERROR = partial(failure, 500, msg="Internal Error")