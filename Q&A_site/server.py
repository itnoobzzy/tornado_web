#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : server.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  :

from tornado import (
    web,
    ioloop,
)
from peewee_async import Manager

from qa_site.urls import urlpattern
from qa_site.settings import settings, database

class MainHandler(web.RequestHandler):

    async def get(self, *args, **kwargs):
        pass

    async def post(self, *args, **kwargs):
        pass





if __name__ == '__main__':
    # 集成json到wtfroms中
    import wtforms_json

    wtforms_json.init()

    app = web.Application(urlpattern, debug=True, **settings)

    # 使用异步ORM
    objects = Manager(database)
    database.set_allow_sync(False)
    # 将对象设置为app全局属性
    app.objects = objects

    app.listen(8000)
    ioloop.IOLoop.current().start()