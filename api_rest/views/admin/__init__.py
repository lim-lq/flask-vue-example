# coding=utf-8
"""
desc:   权限管理模块
author: congqing.li
date:   2016-10-27

"""
import views

url_patterns = [
    (views.UserList, "/users", "admin_user_list"),
    (views.UserDetail, "/users/<int:user_id>", "admin_user_detail"),
    (views.PermissionList, "/permissions", "admin_permission_list"),
    (views.RoleList, "/roles", "admin_role_list"),
    (views.RoleDetail, "/roles/<int:role_id>/", "admin_role_detail"),
    (views.RolePermissionList, "/roles/<int:role_id>/permissions", "admin_role_permission_list"),
    (views.RolePermissionDetail,
     "/roles/<int:role_id>/permissions/<int:permission_id>", "admin_role_permission_detail"),
    (views.UserRoleList, "/users/<int:user_id>/roles", "admin_user_role_list"),
    (views.UserRoleDetail, "/users/<int:user_id>/roles/<int:role_id>", "admin_user_role_detail"),
    (views.RoleUserList, "/roles/<int:role_id>/users", "admin_role_user_list"),
    (views.RoleUserDetail, "/roles/<int:role_id>/users/<int:user_id>", "admin_role_user_detail")
]
