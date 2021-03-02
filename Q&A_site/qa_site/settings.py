#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : settings.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : 配置文件

import peewee_async

# 如果配置内容过多，可以将配置内容写入字典中然后在启动应用的时候以解包的方式传递使用
settings = {
    # 静态文件路径，即使访问static文件夹下子文件里的静态文件也是可以的
    "static_path": "C:/Users/ZZY/Desktop/code/chapter03/static",
    # 访问静态文件url， 不写默认为/static/
    "static_url_prefix": "/static/",
    # 模板路径配置文件
    "template_path": "templates",
    "db": {
        "host": "139.196.161.70",
        "user": "root",
        "password": "root",
        "db": "my_db",
        "port": 3306
    },
    "redis": {
        "host": "127.0.0.1"
    },
    "jwt_expire": 7*24*3600,
    "secret_key":"ZGGA#Mp4yL4w5CDu",
}

database = peewee_async.MySQLDatabase(
    'my_db', host='139.196.161.70', port=3306, user="root", password="root"
)
