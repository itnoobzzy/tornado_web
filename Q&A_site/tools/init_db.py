#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : init_db.py
# @Author: itnoobzzy
# @Date  : 2021/3/1
# @Desc  : 初始化数据库

from peewee import MySQLDatabase

from apps.users.models import User
from qa_site.settings import database
from apps.community.models import CommunityGroup, CommunityGroupMember

database = MySQLDatabase(
    'my_db', host="127.0.0.1", port=3306, user="root", password="root"
)

def init():
    # database.create_tables([User])
    database.create_tables([CommunityGroup, CommunityGroupMember])

if __name__ == '__main__':
    init()
