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

from qa_site.urls import urlpattern
from qa_site.settings import settings

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
    app.listen(8000)
    ioloop.IOLoop.current().start()