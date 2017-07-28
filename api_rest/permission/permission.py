# coding=utf-8

"""
desc:   user permission modal
author: congqing.li
date:   2015-12-31

"""
from collections import namedtuple
from functools import wraps

from flask import g

Needs = namedtuple("Needs", ["name", "desc"])

VIEWNEEDS = Needs("view", u"查看权限")

MANAGENEEDS = Needs("manage", u"管理权限")


class Identity(object):
    def __init__(self, user, permissions):
        self.user = user
        self.permission_map = {}
        self._set_permissions(permissions)

    def _set_permissions(self, permissions):
        self.permission_map = {}
        for _permission in permissions:
            if _permission.name not in self.permission_map.keys():
                self.permission_map[_permission.name] = set()
            self.permission_map[_permission.name].add(_permission.needs)

    def set_permissions(self, permissions):
        self._set_permissions(permissions)

    @property
    def permissions(self):
        return self.permission_map

    def can(self, permission):
        if self.user.is_superuser:
            return True
        if permission.name in self.permission_map.keys():
            if permission.needs in self.permission_map[permission.name]:
                return True

        return False


class Permission(object):
    _total_permissions = set()

    @property
    def permissions(self):
        return Permission._total_permissions

    def add_permission(self, permission):
        Permission._total_permissions.add(permission)


class ItemPermission(Permission):
    def __init__(self, name, display_name, needs):
        self.name = name
        if display_name:
            self.display_name = display_name
        else:
            self.display_name = name

        self.needs = needs

        self.add_permission(self)

    def __str__(self):
        return "<%r> - %s (%s)" % (self.name, self.display_name, str(self.needs))

    def __repr__(self):
        return "<%r> - %r (%r)" % (self.name, self.display_name, self.needs)

    def __eq__(self, other):
        if self.name == other.name and self.display_name == other.display_name and self.needs == other.needs:
            return True
        else:
            return False

    def to_dict(self):
        return {
            "name": self.name,
            "needs": self.needs
        }

    def require(self, func):
        @wraps(func)
        def _decorator(*args, **kwargs):
            if hasattr(g, "identity") and g.identity.can(self):
                return func(*args, **kwargs)
            else:
                return {"status": "failure", "result": {"error": u"抱歉，您没有权限"}}, 403
        return _decorator
