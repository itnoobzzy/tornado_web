#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : url 配置

from apps.users import urls as user_urls
from apps.community import urls as community_urls

urlpattern = []

urlpattern += user_urls.urlpattern
urlpattern += community_urls.urlpattern