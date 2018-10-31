#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/10/30 下午3:11.
"""
from flask import redirect, url_for
from apps.api.urls import api


# 蓝图注册
def init_app(app):
    app.add_url_rule('/', view_func=lambda: redirect(url_for('api.ping')))
    app.register_blueprint(api, url_prefix='/api', strict_slashes=False)
