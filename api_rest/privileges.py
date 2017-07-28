# coding=utf-8
"""
desc:   定义权限
author: congqing.li
date:   2016-10-31

"""
from permission.permission import ItemPermission, VIEWNEEDS, MANAGENEEDS


# 权限管理模块的查看权限
admin_view = ItemPermission("admin", u"用户角色管理", VIEWNEEDS)

# 权限管理模块的管理权限
admin_manage = ItemPermission("admin", u"用户角色管理", MANAGENEEDS)

# 学生管理权限
student_manage = ItemPermission("student", u"学生管理", MANAGENEEDS)
