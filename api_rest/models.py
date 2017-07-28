# coding=utf-8
"""
desc:   database model define

"""

import hashlib
import datetime

from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired

from flask import current_app

from applications import db
from error_handlers import ObjectNotExists, TokenExpired, BadToken
from api_rest import http_responses


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


##############################################################################
#                       Begin 权限管理模块
##############################################################################
class Role(BaseModel, db.Model):
    """
    desc:   角色表

    """
    name = db.Column(db.String(20))
    comment = db.Column(db.String(100))

    def __init__(self, name, comment):
        self.name = name
        self.create_date = datetime.datetime.now()
        self.modify_date = datetime.datetime.now()
        self.comment = comment

    def to_dict(self):
        return self._to_dict(name=self.name, comment=self.comment)

    def update(self, **kwargs):
        """
        desc:   更新角色信息

        """
        self.name = kwargs['name']
        self.comment = kwargs['comment']


class Permission(BaseModel, db.Model):
    """
    desc:   权限表

    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    target = db.Column(db.String(20))
    target_desc = db.Column(db.String(50))
    permission = db.Column(db.String(10))
    permission_desc = db.Column(db.String(50))

    def __init__(self, target, target_desc, permission, permission_desc):
        self.target = target
        self.target_desc = target_desc
        self.permission = permission
        self.permission_desc = permission_desc

    def __eq__(self, other):
        if other.target == self.target and other.target_desc == self.target_desc \
                and other.permission == self.permission and other.permission_desc == self.permission_desc:
            return True
        else:
            return False

    def to_dict(self):
        return self._to_dict(target=self.target, target_desc=self.target_desc,
                             permission=self.permission, premission_desc=self.permission_desc)


class RolesPermissions(BaseModel, db.Model):
    """
    desc:   角色权限关联表

    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role", backref=db.backref("roles_permissions", lazy="dynamic"))
    permission_id = db.Column(db.Integer, db.ForeignKey("permission.id"))
    permission = db.relationship("Permission", backref=db.backref("roles_permissions", lazy="dynamic"))

    def __init__(self, role, permission):
        self.role = role
        self.permission = permission


class User(BaseModel, db.Model):
    username = db.Column(db.String(20), unique=True)
    nickname = db.Column(db.String(30))
    password = db.Column(db.String(32))
    email = db.Column(db.String(255), default="")
    is_superuser = db.Column(db.Boolean, default=False)

    def __init__(self, username, nickname, password, email, create_date=None, modify_date=None, is_superuser=False):
        self.username = username
        self.nickname = nickname if nickname else username
        self.create_date = create_date if create_date else datetime.datetime.now()
        self.modify_date = modify_date if modify_date else datetime.datetime.now()
        self.password = self._hash_password(password)
        self.email = email
        self.is_superuser = is_superuser

    def _hash_password(self, password):
        key = "%s%s" % (password, 'SECRET')
        return hashlib.md5(key).hexdigest()

    def verify_password(self, password):
        return self.password == self._hash_password(password)

    def update_password(self, password):
        self.password = self._hash_password(password)

    def update(self, **kwargs):
        self.username = kwargs['username']
        if kwargs.get("email"):
            self.email = kwargs["email"]
        if kwargs.get("nickname"):
            self.nickname = kwargs["nickname"]

    def to_dict(self):
        return self._to_dict(username=self.username, nickname=self.nickname, email=self.email)

    def generate_auth_token(self):
        """
        desc:   生成登录用户的token
        params: user_id     用户唯一标识号
        return: token
        date:   2016-10-28

        """
        s = TimedJSONWebSignatureSerializer(current_app.config.get("SECRET_KEY", "No secret key"),
                                            current_app.config.get("USER_TOKEN_EXPIRATION", 3600))

        return s.dumps({"user_id": self.id})

    @classmethod
    def verify_auth_token(cls, token):
        s = TimedJSONWebSignatureSerializer(current_app.config.get("SECRET_KEY", "No secret key"))
        try:
            data = s.loads(token)
        except SignatureExpired:
            raise TokenExpired(http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"Token过期了，请重新登录"}))
        except BadSignature:
            raise BadToken(http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"Token无效，请重新登录"}))

        try:
            user = User.get_object(id=data["user_id"])
        except ObjectNotExists:
            raise BadToken(http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"Token无效，请重新登录"}))
        return user


class UsersRoles(BaseModel, db.Model):
    """
    desc:   用户角色关联表

    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("user_roles", lazy="dynamic", cascade="all, delete-orphan"))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role", backref=db.backref("role_users", lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, user, role):
        self.user = user
        self.role = role
##############################################################################
#                       End 权限管理模块
##############################################################################


class Students(BaseModel, db.Model):
    """
    desc:   学生表模型

    """
    name = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return self._to_dict(name=self.name)
