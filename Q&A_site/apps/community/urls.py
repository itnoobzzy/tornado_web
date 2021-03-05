#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : users url配置

from tornado.web import url

from apps.community.handler import (
    GroupHandler,
    GroupMemberHandler,
    GroupDetailHandler,
    PostHandler
)

urlpattern = (
    url("/groups/", GroupHandler),
    url("/groups/([0-9]+)/", GroupDetailHandler),
    url("/groups/([0-9]+)/members/", GroupMemberHandler),
    # 发表帖子
    url("/groups/([0-9]+)/posts/", PostHandler)
)