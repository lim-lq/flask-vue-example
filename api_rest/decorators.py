# coding=utf-8
"""
desc:   自定义装饰器
author: congqing.li
date:   2016-10-27

"""
import pickle
from functools import wraps

from flask import request, g
from api_rest.models import User
from api_rest import error_handlers
from api_rest import http_responses


def login_required(func):
    """
    desc:   登录认证装饰器

    """
    @wraps(func)
    def _decorator_func(*args, **kwargs):
        if request.authorization is None:
            content_type = request.headers["Content-Type"]
            if "application/x-www-form-urlencoded" in content_type:
                data = request.form.to_dict()
            elif "application/json" in content_type:
                data = request.get_json()
            elif "multipart/form-data" in content_type:
                data = request.get_json()
                if data is None:
                    data = request.form.to_dict()
            else:
                raise error_handlers.BadToken(http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"认证失败"}))
            if not isinstance(data, dict):
                raise error_handlers.BadToken(http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"请传递json格式数据"}))
            token = data.get("token", None)
            if token is None:
                raise error_handlers.MissToken(
                    http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"认证失败，没有token"})
                )
        else:
            token = request.authorization["username"]

        g.user = User.verify_auth_token(token)

        # 用户权限
        identity = g.cache.get(token)

        if identity is not None:
            g.identity = pickle.loads(identity)
        return func(*args, **kwargs)

    return _decorator_func
