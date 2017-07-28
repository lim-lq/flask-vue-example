# coding=utf-8
"""
desc:   命令函数定义
author: congqing.li
date:   2016-10-31

"""
import os

from flask_script import Command, prompt, prompt_pass

from api_rest import models
from permission.permission import Permission
from api_rest.applications import app, db
# 该引用保证所有权限都引入进来
from api_rest.privileges import *


class SavePermission(Command, Permission):
    """
    desc:   初始化存储权限项

    """
    def run(self):
        with app.app_context():
            g_db = db.session

            # 之前数据库中的所有权限
            old_permissions = models.Permission.query.all()

            for _permission in Permission._total_permissions:
                permission = models.Permission(_permission.name, _permission.display_name,
                                               _permission.needs.name, _permission.needs.desc)
                if permission not in old_permissions:
                    g_db.add(permission)
                else:
                    old_permissions.remove(permission)

            for _permission in old_permissions:
                g_db.delete(_permission)
            g_db.commit()


class CreateSuperuser(Command):
    """
    desc:   创建超级管理员

    """
    def run(self):
        username = prompt("请输入用户名")
        with app.app_context():
            g_db = db.session
            while True:
                old_user = models.User.query.filter_by(username=username).first()
                if old_user:
                    print "用户名重复"
                    username = prompt("请重新输入用户名")
                else:
                    break
            nickname = prompt("请输入昵称")
            while True:
                password = prompt_pass("请输入密码")
                confirm_password = prompt_pass("再次输入密码")
                if password != confirm_password:
                    print "创建失败, 两次密码不一致"
                    continue
                break

            super_user = models.User(username, nickname, password, "", is_superuser=True)
            g_db.add(super_user)
            g_db.commit()
            print super_user.create_date.strftime("%Y%m%d%H%M%S")
            print "创建超级用户：%s成功" % username