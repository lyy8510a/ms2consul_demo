#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/10/30 下午5:25.
"""
from flask_jsonrpc import JSONRPC

jsonrpc = JSONRPC()


@jsonrpc.method('App.index')
def index():
    """
        How to user:

        from flask_jsonrpc.proxy import ServiceProxy

        server = ServiceProxy('http://localhost:10110/api')

        print(server.App.index())

    """
    return u'Welcome to Flask JSON-RPC'



