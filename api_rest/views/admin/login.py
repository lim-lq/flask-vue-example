# coding=utf-8
"""
desc:   登录模块
author: congqing.li
date:   2016-10-28

"""
from flask import g
from flask_restful import Resource

from api_rest import http_responses
from api_rest.models import User
from api_rest.decorators import login_required
from api_rest.views.admin.parsers import login_parser
from api_rest.utils import cache_user_privileges


class Login(Resource):
    def post(self):
        args = login_parser.parse_args()
        _user = User.get_object(username=args.username)
        if not _user.verify_password(args.password):
            return http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"密码错误"})

        token = _user.generate_auth_token()
        g.user = _user
        # 设置用户权限到缓存
        # if not hasattr(g, "identity"):
        _permissions = cache_user_privileges(token)
        permissions = set()
        for per in _permissions:
            permissions.add(".".join([per.name, per.needs.name]))

        return http_responses.HTTP_200_OK(msg={"message": "Login success",
                                               "username": _user.username,
                                               "nickname": _user.nickname,
                                               "id": _user.id,
                                               "is_superuser": _user.is_superuser,
                                               "permissions": list(permissions),
                                               "token": token})

    @login_required
    def get(self):
        return http_responses.HTTP_200_OK()
