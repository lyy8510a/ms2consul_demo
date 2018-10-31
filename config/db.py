#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/10/30 下午4:02.
"""


class Config(object):
    # 数据库配置(本地)
    MYSQL_HOST = '127.0.0.1'  # 此处修改为您的mysql的主机IP
    MYSQL_PORT = 3306  # 此处修改为您的mysql的主机端口
    MYSQL_USER = 'root'  # 此处修改为您的mysql的用户名称
    MYSQL_PASS = '123456'  # 此处修改为您的mysql的用户密码
    MYSQL_DB = 'messer'  # 此处修改为您的mysql的数据库名称

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8".format(MYSQL_USER, MYSQL_PASS,
                                                                                        MYSQL_HOST
                                                                                        , MYSQL_PORT, MYSQL_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    pass


config = DevConfig()
