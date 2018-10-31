#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/10/30 下午2:59.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """Base config class."""
    # 版本
    VERSION = 'beta 0.1'
    # 项目名称
    PROJECTNAME = 'micoservice-demo'
    # 端口
    PORT = 10110
    # json中文不乱码
    JSON_AS_ASCII = False
    # 秘钥
    SECRET_KEY = os.urandom(24)
    # 启动超时时间
    START_TIMEOUT = 15
    # Consul tag
    CONSUL_TAG = ['python-mico-service']


class SitConfig(Config):
    # 部署机器的IP
    HOST = '127.0.0.1'
    # 是否开启调试状态，本项目会产生2个进程
    DEBUG = True
    # 是否开启守护进程
    DAEMON = False
    # 起几个进程
    WORKERS = 1
    # Consul info
    CONSUL_HOST = 'localhost'
    CONSUL_PORT = 8500

# Default using Config settings, you can write if/else for different env
config = SitConfig()
