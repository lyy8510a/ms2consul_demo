#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/10/30 下午3:12.
"""
from flask import current_app as app, request, views
from utils.layout import outputJsonByMessage
from utils.consulclient import ConsulClient


class PingView(views.MethodView):

    def get(self):
        app.logger.info(request.endpoint)  # 日志用法
        return outputJsonByMessage("S", "Ping", "Pong")


class ServiceView(views.MethodView):
    def get(self):
        """列出所有服务"""
        try:
            client = ConsulClient(app.config['CONSUL_HOST'], app.config['CONSUL_PORT'])
            services = client.getServices()
            return outputJsonByMessage("S",
                                       "已经注册的服务，通过Address和Port就可以知道服务的调用地址啦，有api网关的话，可以直接根据api网关地址+集群名称+endpoint 调用",
                                       services)
        except Exception as e:
            app.logger.error(str(e))
            return outputJsonByMessage("E", str(e))

    def post(self):
        """列出指定服务"""
        try:
            name = request.values.get('name')
            client = ConsulClient(app.config['CONSUL_HOST'], app.config['CONSUL_PORT'])
            service = client.getService(name)
            return outputJsonByMessage("S",
                                       "已经注册的服务，通过Address和Port就可以知道服务的调用地址啦，有api网关的话，可以直接根据api网关地址+集群名称+endpoint 调用",
                                       service)
        except Exception as e:
            app.logger.error(str(e))
            return outputJsonByMessage("E", str(e))
