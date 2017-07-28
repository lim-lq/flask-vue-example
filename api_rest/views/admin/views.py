# coding=utf-8
"""
desc:   权限管理视图
author: congqing.li
date:   2016-10-27

"""
from flask import g
from flask_restful import Resource

from api_rest.views.admin.parsers import user_parser, user_modify_parser, batch_delete_user_parser, role_parser, \
    role_permissions_parser, user_roles_parser, role_users_parser, batch_delete_role_parser
from api_rest.models import User, Permission, Role, RolesPermissions, UsersRoles
from api_rest import http_responses
from api_rest.decorators import login_required
from api_rest.privileges import admin_manage


class UserList(Resource):
    """
    desc:   get     获取用户列表
            post    添加用户
            delete  批量删除用户

    """
    decorators = [login_required]

    def get(self):
        users = User.query.filter_by(is_superuser=0).all()
        user_list = []
        for user in users:
            user_roles = UsersRoles.query.filter_by(user_id=user.id).all()
            role_str = ';'.join([user_role.role.name for user_role in user_roles])
            user = user.to_dict()
            user["role"] = role_str
            user_list.append(user)
        return http_responses.HTTP_200_OK(msg={
            "users": user_list
        })

    @admin_manage.require
    def post(self):
        args = user_parser.parse_args()
        # 检查user是否存在
        _user = User.query.filter_by(username=args.username).first()
        if _user:
            return http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"用户名已存在 - %s" % args.username})
        user = User(**args)
        try:
            g.db.add(user)
            g.db.commit()
        except Exception, e:
            return http_responses.HTTP_400_BAD_REQUEST(msg={"error": str(e)})
        return http_responses.HTTP_201_CREATED(msg={"user_id": user.id})

    @admin_manage.require
    def delete(self):
        args = batch_delete_user_parser.parse_args()
        error_users = []
        for user_id in args.user_ids:
            try:
                user_id = int(user_id)
            except ValueError:
                return http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"用户Id必须为整数"})

            user = User.query.filter_by(id=user_id).first()
            if user is None:
                continue
            g.db.delete(user)

        if len(args.user_ids):
            g.db.commit()
        if len(error_users):
            return http_responses.HTTP_400_BAD_REQUEST(msg={"error": "\n".join(error_users)})

        return http_responses.HTTP_200_OK(msg="Delete success")


class UserDetail(Resource):
    """
    desc:   delete  删除指定用户
            put     修改用户信息

    """
    decorators = [login_required]

    @admin_manage.require
    def delete(self, user_id):
        _user = User.get_object(id=user_id)
        g.db.delete(_user)
        g.db.commit()
        return http_responses.HTTP_200_OK()

    @admin_manage.require
    def put(self, user_id):
        _user = User.get_object(id=user_id)
        args = user_modify_parser.parse_args()
        _user.username = args.username
        if args.nickname is not None:
            _user.nickname = args.nickname
        if args.email is not None:
            _user.email = args.email
        g.db.commit()
        return http_responses.HTTP_200_OK(msg=u"修改用户信息成功")


class PermissionList(Resource):
    """
    desc:   get 获取权限列表

    """
    decorators = [login_required]

    def get(self):
        permissions = Permission.query.all()
        permissions = [permission.to_dict() for permission in permissions]
        permissions = sorted(permissions, key=lambda item: item["target"])

        return http_responses.HTTP_200_OK(msg={"permissions": permissions})


class RoleList(Resource):
    """
    desc:   get     获取角色列表
            post    添加角色
            delete  批量删除

    """
    decorators = [login_required]

    def get(self):
        roles = Role.query.all()
        roles = [role.to_dict() for role in roles]

        return http_responses.HTTP_200_OK(msg={"roles": roles})

    @admin_manage.require
    def post(self):
        args = role_parser.parse_args()
        _role = Role.query.filter_by(name=args.name).first()
        if _role:
            return http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"角色已存在 - %s" % args.name})

        role = Role(**args)
        g.db.add(role)
        g.db.commit()

        return http_responses.HTTP_200_OK()

    @admin_manage.require
    def delete(self):
        args = batch_delete_role_parser.parse_args()

        error_roles = []
        for role_id in args.role_ids:
            try:
                role_id = int(role_id)
            except ValueError:
                return http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"角色Id必须为整数 - %s" % role_id})

            role = Role.query.filter_by(id=role_id).first()
            if role is None:
                continue
            # 判断是否有用户关联
            if UsersRoles.query.filter_by(role_id=role_id).count() > 0:
                error_roles.append(u"角色: %s 有用户关联不能删除" % role.name)
                continue
            g.db.delete(role)

        if len(args.role_ids):
            g.db.commit()

        if len(error_roles):
            return http_responses.HTTP_400_BAD_REQUEST(msg={"error": "\n".join(error_roles)})

        return http_responses.HTTP_200_OK(msg="Delete success")


class RoleDetail(Resource):
    """
    desc:   get     获取角色详细信息
            put     更新角色信息

    """
    decorators = [login_required]

    def get(self, role_id):
        role = Role.get_object(id=role_id)
        return http_responses.HTTP_200_OK(msg={"role": role.to_dict()})

    @admin_manage.require
    def put(self, role_id):
        role = Role.get_object(id=role_id)
        args = role_parser.parse_args()
        role.update(**args)
        g.db.commit()

        return http_responses.HTTP_200_OK(msg="Modify success")


class RolePermissionList(Resource):
    """
    desc:   get     获取指定角色的权限列表
            post    为指定角色添加权限
            delete  批量删除指定角色的权限
            put     更新指定角色的权限

    """
    decorators = [login_required]

    def get(self, role_id):
        role = Role.get_object(id=role_id)

        role_permissions = RolesPermissions.query.filter_by(role_id=role_id).all()
        role_permissions = [_role_per.permission.to_dict() for _role_per in role_permissions]

        return http_responses.HTTP_200_OK(msg={"role": role.name, "permissions": role_permissions})

    @admin_manage.require
    def post(self, role_id):
        args = role_permissions_parser.parse_args()

        role = Role.get_object(id=role_id)

        for permission_id in args.permission_ids:
            try:
                p_id = int(permission_id)
            except ValueError:
                return http_responses.HTTP_400_BAD_REQUEST(
                    msg={"error": u"权限id'%s'必须为整数" % permission_id}
                )
            if RolesPermissions.query.filter_by(role_id=role_id, permission_id=p_id).first():
                continue

            permission_obj = Permission.get_object(id=p_id)
            role_permission = RolesPermissions(role, permission_obj)
            g.db.add(role_permission)
        if len(args.permission_ids):
            g.db.commit()

        return http_responses.HTTP_200_OK()

    @admin_manage.require
    def delete(self, role_id):
        args = role_permissions_parser.parse_args()

        for per_id in args.permission_ids:
            try:
                per_id = int(per_id)
            except ValueError:
                return http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"权限Id必须为整数"})
            role_permission = RolesPermissions.query.filter_by(role_id=role_id, permission_id=per_id)
            if role_permission:
                g.db.delete(role_permission)
        if len(args.permission_ids):
            g.db.commit()
        return http_responses.HTTP_200_OK(msg="delete success")

    @admin_manage.require
    def put(self, role_id):
        args = role_permissions_parser.parse_args()

        role = Role.get_object(id=role_id)

        all_role_permissions = RolesPermissions.query.filter_by(role_id=role_id).all()

        if args.permission_ids:
            all_permission_ids = set([role_per.permission.id for role_per in all_role_permissions])
            new_permission_ids = set(args.permission_ids)

            add_permission_ids = new_permission_ids - all_permission_ids
            delete_permission_ids = all_permission_ids - new_permission_ids

            # 删除权限
            for per_id in delete_permission_ids:
                g.db.delete(filter(lambda x: x.permission_id == per_id, all_role_permissions)[0])

            # 新增权限
            for per_id in add_permission_ids:
                permission = Permission.query.filter_by(id=per_id).first()
                if permission is None:
                    continue
                role_permission = RolesPermissions(role=role, permission=permission)
                g.db.add(role_permission)
        else:
            for role_per in all_role_permissions:
                g.db.delete(role_per)

        g.db.commit()
        return http_responses.HTTP_200_OK(msg="Update role permission success")


class RolePermissionDetail(Resource):
    """
    desc:   delete  单一删除指定角色的指定权限

    """
    decorators = [login_required]

    @admin_manage.require
    def delete(self, role_id, permission_id):
        role_permission = RolesPermissions.get_object(role_id=role_id, permission_id=permission_id)
        g.db.delete(role_permission)
        g.db.commit()
        return http_responses.HTTP_200_OK()


class RoleUserList(Resource):
    """
    desc:   get     获取指定角色包含的用户列表
            post    为指定角色批量添加用户
            delete  批量删除指定角色的用户

    """
    decorators = [login_required]

    def get(self, role_id):
        role = Role.get_object(id=role_id)
        user_roles = UsersRoles.query.filter_by(role_id=role_id).all()

        users = [user_role.user.to_dict() for user_role in user_roles]

        return http_responses.HTTP_200_OK(msg={"role": role.name, "users": users})

    @admin_manage.require
    def post(self, role_id):
        args = role_users_parser.parse_args()
        role = Role.get_object(id=role_id)

        for user_id in args.user_ids:
            try:
                user_id = int(user_id)
            except ValueError:
                return http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"用户Id必须为整数"})
            if UsersRoles.query.filter_by(user_id=user_id, role_id=role_id).first():
                continue

            user = User.get_object(id=user_id)
            user_role = UsersRoles(user, role)
            g.db.add(user_role)

        if len(args.user_ids):
            g.db.commit()

        return http_responses.HTTP_200_OK()

    @admin_manage.require
    def delete(self, role_id):
        args = role_users_parser.parse_args()

        for user_id in args.user_ids:
            try:
                user_id = int(user_id)
            except ValueError:
                return http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"用户Id必须为整数"})
            user_role = UsersRoles.query.filter_by(user_id=user_id, role_id=role_id).first()
            if user_role:
                g.db.delete(user_role)
        if len(args.user_ids):
            g.db.commit()

        return http_responses.HTTP_200_OK(msg="delete success")


class RoleUserDetail(Resource):
    """
    desc:   delete  单一删除指定角色的指定用户

    """
    decorators = [login_required]

    @admin_manage.require
    def delete(self, role_id, user_id):
        user_role = UsersRoles.get_object(user_id=user_id, role_id=role_id)
        g.db.delete(user_role)
        g.db.commit()

        return http_responses.HTTP_200_OK()


class UserRoleList(Resource):
    """
    desc:   get     获取指定用户所属的角色列表
            post    为指定用户批量添加角色
            delete  批量删除指定用户的角色
            put     更新用户角色

    """
    decorators = [login_required]

    def get(self, user_id):
        user = User.get_object(id=user_id)
        user_roles = UsersRoles.query.filter_by(user_id=user_id).all()

        roles = [user_role.role.to_dict() for user_role in user_roles]

        return http_responses.HTTP_200_OK(msg={"user": user.username, "roles": roles})

    @admin_manage.require
    def post(self, user_id):
        args = user_roles_parser.parse_args()
        user = User.get_object(id=user_id)
        for role_id in args.role_ids:
            try:
                role_id = int(role_id)
            except ValueError:
                return http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"角色Id必须为整数"})

            if UsersRoles.query.filter_by(user_id=user_id, role_id=role_id).first():
                continue

            role = Role.get_object(id=role_id)
            user_role = UsersRoles(user, role)
            g.db.add(user_role)

        if len(args.role_ids):
            g.db.commit()

        return http_responses.HTTP_200_OK()

    @admin_manage.require
    def delete(self, user_id):
        args = user_roles_parser.parse_args()
        for role_id in args.role_ids:
            try:
                role_id = int(role_id)
            except ValueError:
                return http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"角色Id必须为整数"})
            user_role = UsersRoles.query.filter_by(user_id=user_id, role_id=role_id).first()
            if user_role:
                g.db.delete(user_role)

        if len(args.role_ids):
            g.db.commit()

        return http_responses.HTTP_200_OK()

    @admin_manage.require
    def put(self, user_id):
        args = user_roles_parser.parse_args()

        user = User.get_object(id=user_id)

        all_user_roles = UsersRoles.query.filter_by(user_id=user_id).all()

        if args.role_ids:
            all_role_ids = set([user_role.role.id for user_role in all_user_roles])
            try:
                new_role_ids = set([int(role_id) for role_id in args.role_ids])
            except ValueError:
                return http_responses.HTTP_400_BAD_REQUEST(msg={"error": u"角色id必须为整数"})

            add_role_ids = new_role_ids - all_role_ids
            delete_role_ids = all_role_ids - new_role_ids

            # 删除角色
            for role_id in delete_role_ids:
                g.db.delete(filter(lambda x: x.role_id == role_id, all_user_roles)[0])

            # 新增角色
            for role_id in add_role_ids:
                role = Role.query.filter_by(id=role_id).first()
                if role is None:
                    continue
                user_role = UsersRoles(user=user, role=role)
                g.db.add(user_role)
        else:
            for user_role in all_user_roles:
                g.db.delete(user_role)

        g.db.commit()
        return http_responses.HTTP_200_OK(msg="Update role permission success")


class UserRoleDetail(Resource):
    """
    desc:   delete  单一删除指定用户的指定角色

    """
    decorators = [admin_manage.require, login_required]

    def delete(self, user_id, role_id):
        user_role = UsersRoles.get_object(user_id=user_id, role_id=role_id)
        g.db.delete(user_role)
        g.db.commit()

        return http_responses.HTTP_200_OK()
