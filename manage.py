#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/8/21 下午3:40.
"""

from flask_script import Manager
from apps import create_app, db
from flask_migrate import Migrate
from utils.helper import start_service, register_consul, stop_service, deregister_consul

app = create_app()
migrate = Migrate(app, db)  # 第二课新增

app.debug = app.config["DEBUG"]

# Init manager object via app object
manager = Manager(app)


@manager.command
def runserver():  # 第二课新增
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    try:

        # 获取根目录config.py的配置项
        register_consul()
        start_service('gunicorn')


    except Exception as e:
        raise e


@manager.command
def stopserver():  # 第二课新增
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    try:
        deregister_consul()
        stop_service('gunicorn')

    except Exception as e:
        raise e


@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    # 确保有导入 Flask app object，否则启动的 CLI 上下文中仍然没有 app 对象
    return dict(app=app, db=db)  # 第二课新增


# 创建数据库脚本
@manager.command
def create_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.create_all()
    db.session.commit()


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    manager.run()
