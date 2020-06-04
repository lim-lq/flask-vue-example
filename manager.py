# coding=utf-8
"""
desc:   run server script for test
author: levi-lq
date:   2017-05-23

"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api_rest.command import SavePermission, CreateSuperuser
from api_rest import app

manager = Manager(app)
# migrate database command
manager.add_command("db", MigrateCommand)
manager.add_command("init_privilege", SavePermission)
manager.add_command("create_superuser", CreateSuperuser)


if __name__ == "__main__":
    manager.run()
