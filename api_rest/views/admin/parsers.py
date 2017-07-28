# coding=utf-8
"""
desc:   解析请求admin api的数据
author: congqing.li
date:   2016-10-27

"""
from flask_restful import reqparse
from api_rest.parser_types import string

# 添加用户时的参数解析
user_parser = reqparse.RequestParser()
user_parser.add_argument("username", type=string(20), required=True)
user_parser.add_argument("nickname", type=string(30))
user_parser.add_argument("email", type=string(255))
user_parser.add_argument("password", type=string(20), required=True)

# 修改用户信息时的参数解析
user_modify_parser = reqparse.RequestParser()
user_modify_parser.add_argument("username", default="", type=string(20))
user_modify_parser.add_argument("nickname", default="", type=string(30))
user_modify_parser.add_argument("email", default="", type=string(255))

# 批量删除用户时的参数解析
batch_delete_user_parser = reqparse.RequestParser()
batch_delete_user_parser.add_argument("user_ids", required=True, action="append")

# 添加用户组时的参数解析
role_parser = reqparse.RequestParser()
role_parser.add_argument("name", required=True)
role_parser.add_argument("comment", default="")

# 批量删除角色时参数解析
batch_delete_role_parser = reqparse.RequestParser()
batch_delete_role_parser.add_argument("role_ids", required=True, action="append")

# 登录的参数解析
login_parser = reqparse.RequestParser()
login_parser.add_argument("username", required=True)
login_parser.add_argument("password", required=True)

# 添加用户组与权限关联关系的参数解析
role_permissions_parser = reqparse.RequestParser()
role_permissions_parser.add_argument("permission_ids", type=int, action="append")

# 添加用户与用户组关联关系的参数解析
user_roles_parser = reqparse.RequestParser()
user_roles_parser.add_argument("role_ids", action="append")

# 添加用户组与用户关联关系的参数解析
role_users_parser = reqparse.RequestParser()
role_users_parser.add_argument("user_ids", required=True, action="append")
