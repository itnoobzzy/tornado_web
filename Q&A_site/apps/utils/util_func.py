#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : util_func.py
# @Author: itnoobzzy
# @Date  : 2021/3/5
# @Desc  : json dumps时间

from datetime import date, datetime

def json_serial(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError("Type {}s not serializable".format(type(obj)))