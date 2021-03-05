#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : models.py
# @Author: itnoobzzy
# @Date  : 2021/3/1
# @Desc  : users 模型类

from datetime import datetime

from peewee import *

from qa_site.models import BaseModel
from apps.users.models import User


class CommunityGroup(BaseModel):
    creator = ForeignKeyField(User, verbose_name="创建者")
    name = CharField(max_length=100, null=True, verbose_name="名称")
    category = CharField(max_length=20, verbose_name="分类", null=True)
    front_image = CharField(max_length=200, null=True, verbose_name="封面图")
    desc = TextField(verbose_name="简介")
    notice = TextField(verbose_name="公告")

    #小组的信息
    member_nums = IntegerField(default=0, verbose_name="成员数")
    post_nums = IntegerField(default=0, verbose_name="帖子数")

    @classmethod
    def extend(cls):
        """
        在使用异步ORM驱动的时候model_to_dict方法无法处理外键，需要通过join字句关联外键对象生成一个预处理查询集
        :return:
        """
        return cls.select(cls, User.id, User.nick_name).join(User)

HANDLE_STATUS = (
    ("agree", "同意"),
    ("refuse", "拒绝")
)
class CommunityGroupMember(BaseModel):
    user = ForeignKeyField(User, verbose_name="用户")
    community = ForeignKeyField(CommunityGroup, verbose_name="社区")
    status = CharField(choices=HANDLE_STATUS, max_length=10, null=True, verbose_name="处理状态")
    handle_msg = CharField(max_length=200, null=True, verbose_name="处理内容")
    apply_reason = CharField(max_length=200, verbose_name="申请理由")
    handle_time = DateTimeField(default=datetime.now(), verbose_name="加入时间")