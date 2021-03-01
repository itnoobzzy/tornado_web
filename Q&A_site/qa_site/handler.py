#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : handler.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : 全局handler

from tornado.web import RequestHandler
import redis

class RedisHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(RedisHandler, self).__init__(application, request, **kwargs)
        self.redis_conn = redis.StrictRedis(**self.settings["redis"])