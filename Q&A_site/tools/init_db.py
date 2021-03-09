#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : init_db.py
# @Author: itnoobzzy
# @Date  : 2021/3/1
# @Desc  : 初始化数据库

from peewee import MySQLDatabase

from apps.users.models import User
from qa_site.settings import database
from apps.community.models import *
from apps.question.models import *

database = MySQLDatabase(
    'my_db', host="139.196.161.70", port=3306, user="root", password="root"
)

def init():
    # database.create_tables([User])
    database.create_tables([Post, PostComment, CommentLike])
    database.create_tables([Post, PostComment, CommentLike, Question, Answer])

if __name__ == '__main__':
    init()
