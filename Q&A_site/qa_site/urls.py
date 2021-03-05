#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : url 配置

from tornado.web import (
    url,
    StaticFileHandler
)

from apps.users import urls as user_urls
from apps.community import urls as community_urls
from qa_site.settings import settings

urlpattern = [
    (url("/media/(.*)", StaticFileHandler, {'path': settings["MEDIA_ROOT"]}))
]

urlpattern += user_urls.urlpattern
urlpattern += community_urls.urlpattern