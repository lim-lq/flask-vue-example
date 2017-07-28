# coding=utf-8
"""
desc:   utils model

"""
import os
import pickle

from flask import g, current_app

from api_rest.models import UsersRoles, RolesPermissions
from api_rest.permission.permission import ItemPermission, Needs, Permission, Identity


def register_route(api, url_prefix, url_patterns):
    """
    desc:   在主应用中注册模块路由
    params: api             flask_restful 的实例
            url_prefix      路由前缀
            url_patterns    具体的url

    """
    for url in url_patterns:
        if len(url) == 3:
            api.add_resource(url[0], os.path.join(url_prefix, url[1]), endpoint=url[2])
        else:
            api.add_resource(url[0], os.path.join(url_prefix, url[1]))


def cache_user_privileges(token):
    """
    desc:   缓存用户的权限到redis中
            数据结构：
                 key            value
                <token>        Identity(user, permissions)
    params: token   用户缓存

    """
    item_permission_list = []
    if not g.user.is_superuser:
        user_roles = UsersRoles.query.filter_by(user_id=g.user.id).all()
        all_permissions = []
        for user_role in user_roles:
            role_permission = RolesPermissions.query.filter_by(role_id=user_role.role.id).all()
            all_permissions.extend(role_permission)

        for per in all_permissions:
            per = ItemPermission(per.permission.target, per.permission.target_desc,
                                 Needs(per.permission.permission, per.permission.permission_desc))
            item_permission_list.append(per)

    data = {token: pickle.dumps(Identity(g.user, item_permission_list))}
    g.cache.set(expire=current_app.config["USER_TOKEN_EXPIRATION"], **data)

    if g.user.is_superuser:
        item_permission_list = Permission._total_permissions
    return item_permission_list
