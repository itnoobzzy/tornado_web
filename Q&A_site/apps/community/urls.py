#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : users url配置

from tornado.web import url

from apps.community.handler import (
    GroupHandler
)

urlpattern = (
    url("/groups/", GroupHandler),
)