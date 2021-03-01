#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : models.py
# @Author: itnoobzzy
# @Date  : 2021/3/1
# @Desc  : 模型类基类

from datetime import datetime

from qa_site.settings import database
from peewee import *

class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        database = database