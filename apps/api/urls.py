#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/10/30 下午3:05.
"""

from flask import Blueprint
from apps.api import views

api = Blueprint('api', __name__)

api.add_url_rule('/ping', view_func=views.PingView.as_view('ping'))
api.add_url_rule('/services', view_func=views.ServiceView.as_view('services'))
