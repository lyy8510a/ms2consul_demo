#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/10/30 下午2:57.
"""
from flask import Flask

from config.config import config
from config.db import config as dbconfig
from config import logger

from apps import urls
from apps.rpc.views import jsonrpc
from apps.models import db


def create_app():
    # 初始化项目实例
    app = Flask(__name__)
    app.secret_key = app.config['SECRET_KEY']

    # 导入配置项
    app.config.from_object(config)
    app.config.from_object(dbconfig)
    # 注册日志
    logger.init_app(app)
    # 注册蓝图
    urls.init_app(app)
    # 数据库注册
    db.init_app(app)
    # rpc server
    jsonrpc.init_app(app)

    @app.route('/check', methods=['GET'])  # 健康检查url
    def check():
        return 'success'

    return app
